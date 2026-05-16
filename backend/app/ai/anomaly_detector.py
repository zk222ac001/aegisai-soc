import os
import logging
import threading

import joblib
import numpy as np

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# =========================================================
# Logging
# =========================================================

logger = logging.getLogger(__name__)

# =========================================================
# Paths
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "..", "ml_models")
MODEL_PATH = os.path.join(MODEL_DIR, "isolation_forest.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
# =========================================================
# Constants
# =========================================================
DEFAULT_CONTAMINATION = 0.02
TRAINING_SAMPLES = 10000
RANDOM_STATE = 42

SUPPORTED_PROTOCOLS = {
    "TCP": 1,
    "UDP": 2,
    "ICMP": 3
}
# =========================================================
# Anomaly Detector
# =========================================================
class AnomalyDetector:
    def __init__(self):

        self.lock = threading.RLock()
        self.model = IsolationForest(
            n_estimators=200,
            contamination=DEFAULT_CONTAMINATION,
            random_state=RANDOM_STATE,
            n_jobs=-1,
            bootstrap=True
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        # Ensure model directory exists
        os.makedirs(MODEL_DIR, exist_ok=True)
    # =====================================================
    # Generate Training Data
    # =====================================================

    @staticmethod
    def generate_training_data(samples=TRAINING_SAMPLES):
        np.random.seed(RANDOM_STATE)

        training_data = np.column_stack([
            # Source Port
            np.random.randint(1024, 65535, size=samples),
            # Destination Port
            np.random.choice([80, 443, 53, 22, 8080], size=samples),
            # Protocol
            np.random.choice([1, 2, 3], size=samples),
            # Packet Count
            np.random.randint(1, 50, size=samples),
            # Flow Duration
            np.random.randint(1, 5000, size=samples),
            # Bytes
            np.random.randint(64, 5000, size=samples)
        ]).astype(np.float32)
        return training_data
    # =====================================================
    # Train Model
    # =====================================================
    def train(self):
        with self.lock:
            try:
                logger.info("[AI] Training model...")
                training_data = self.generate_training_data()
                scaled_data = self.scaler.fit_transform(training_data)
                self.model.fit(scaled_data)
                # Save model
                joblib.dump(
                    self.model,
                    MODEL_PATH,
                    compress=3
                )
                # Save scaler
                joblib.dump(
                    self.scaler,
                    SCALER_PATH,
                    compress=3
                )
                self.is_trained = True
                logger.info("[AI] Training complete")

            except Exception as e:
                logger.exception(f"[AI] Training failed: {e}")
                raise
    # =====================================================
    # Load Model
    # =====================================================
    def load_model(self):
        with self.lock:
            try:
                if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
                    self.model = joblib.load(MODEL_PATH)
                    self.scaler = joblib.load(SCALER_PATH)
                    self.is_trained = True
                    logger.info("[AI] Model loaded")
                else:
                    logger.warning("[AI] Model not found, training new model")
                    self.train()
            except Exception as e:
                logger.exception(f"[AI] Load failed: {e}")
                raise
    # =====================================================
    # Feature Builder
    # =====================================================
    @staticmethod
    def build_features(
        source_port=0,
        destination_port=0,
        protocol="TCP",
        packet_count=0,
        flow_duration=0,
        bytes_transferred=0
    ):

        protocol_value = SUPPORTED_PROTOCOLS.get(
            str(protocol).upper(),
            0
        )
        features = np.array([

            int(source_port or 0),
            int(destination_port or 0),
            int(protocol_value),
            int(packet_count or 0),
            int(flow_duration or 0),
            int(bytes_transferred or 0)

        ], dtype=np.float32)

        return features
    # =====================================================
    # Predict
    # =====================================================

    def predict(self, features):

        if not self.is_trained:
            self.load_model()
        try:
            with self.lock:
                features = np.asarray(
                    [features],
                    dtype=np.float32
                )
                # Scale
                scaled_features = self.scaler.transform(features)
                # Prediction
                prediction = self.model.predict(scaled_features)
                # Raw score
                raw_score = self.model.decision_function(scaled_features)[0]
                # Convert NumPy bool -> Python bool
                anomaly = bool(prediction[0] == -1)
                # Better scoring logic
                normalized_score = max(
                    0,
                    min(
                        100,
                        int((1 - raw_score) * 50)
                    )
                )
                return {

                    "anomaly": anomaly,
                    "ai_score": float(normalized_score),
                    "risk_score": int(normalized_score)
                }
        except Exception as e:

            logger.exception(f"[AI] Prediction failed: {e}")
            return {
                "anomaly": False,
                "ai_score": 0.0,
                "risk_score": 0,
                "error": str(e)
            }
    # =====================================================
    # Health
    # =====================================================

    def health(self):
        return {
            "trained": bool(self.is_trained),
            "model_exists": os.path.exists(MODEL_PATH),
            "scaler_exists": os.path.exists(SCALER_PATH)
        }

# =========================================================
# Singleton
# =========================================================
detector = AnomalyDetector()