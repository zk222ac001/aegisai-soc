import os
import logging
import threading
import time

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

MODEL_DIR = os.path.join(
    BASE_DIR,
    "..",
    "..",
    "ml_models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "isolation_forest.pkl"
)

SCALER_PATH = os.path.join(
    MODEL_DIR,
    "scaler.pkl"
)

# =========================================================
# Constants
# =========================================================

DEFAULT_CONTAMINATION = 0.03
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
        self.is_trained = False
        self.model = IsolationForest(
            n_estimators=300,
            contamination=DEFAULT_CONTAMINATION,
            random_state=RANDOM_STATE,
            n_jobs=-1,
            bootstrap=True,
            verbose=0
        )
        self.scaler = StandardScaler()
    # =====================================================
    # Training Data Generation
    # =====================================================
    @staticmethod
    def generate_training_data(
        samples=TRAINING_SAMPLES
    ):
        training_data = np.column_stack([
            # Source Port
            np.random.randint(
                1024,
                65535,
                size=samples
            ),
            # Destination Port
            np.random.choice(
                [80, 443, 53, 22],
                size=samples
            ),
            # Protocol
            np.random.choice(
                [1, 2, 3],
                size=samples
            ),
            # Packet Count
            np.random.randint(
                1,
                100,
                size=samples
            ),
            # Flow Duration (ms)
            np.random.randint(
                1,
                5000,
                size=samples
            ),
            # Bytes Transferred
            np.random.randint(
                64,
                1500,
                size=samples
            )
        ]).astype(np.float32)
        return training_data
    # =====================================================
    # Train Model
    # =====================================================
    def train(self):
        with self.lock:
            try:
                logger.info(
                    "[AI] Training Isolation Forest model..."
                )
                os.makedirs(
                    MODEL_DIR,
                    exist_ok=True
                )
                training_data = (
                    self.generate_training_data()
                )
                scaled_data = (
                    self.scaler.fit_transform(
                        training_data
                    )
                )
                self.model.fit(
                    scaled_data
                )
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
                logger.info(
                    "[AI] Model training completed."
                )
            except Exception as e:
                logger.exception(
                    f"[AI] Training failed: {e}"
                )
                raise
    # =====================================================
    # Load Model
    # =====================================================
    def load_model(self):
        with self.lock:
            try:
                model_exists = os.path.exists(MODEL_PATH)
                scaler_exists = os.path.exists(SCALER_PATH)
                if model_exists and scaler_exists:
                    self.model = joblib.load(MODEL_PATH)
                    self.scaler = joblib.load(SCALER_PATH)
                    self.is_trained = True
                    logger.info("[AI] Model loaded successfully.")
                else:
                    logger.warning("[AI] Model not found. Training new model.")
                    self.train()
            except Exception as e:
                logger.exception(
                    f"[AI] Model loading failed: {e}"
                )
                raise
    # =====================================================
    # Feature Builder
    # =====================================================
    @staticmethod
    def build_features(
        *,
        source_port,
        destination_port,
        protocol,
        packet_count,
        flow_duration,
        bytes_transferred
    ):
        
        protocol_value = (SUPPORTED_PROTOCOLS.get(str(protocol).upper(),0))        
        features = np.array([
            source_port or 0,
            destination_port or 0,
            protocol_value,
            packet_count or 0,
            flow_duration or 0,
            bytes_transferred or 0
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
                features = np.asarray([features],dtype=np.float32)
                logger.debug(f"[AI] Features: {features}")
                logger.debug(f"[AI] Feature count:"f"{features.shape[1]}")
                logger.debug(f"[AI] Scaler expects: "f"{self.scaler.n_features_in_}")
                scaled_features = (self.scaler.transform(features))
                prediction = (self.model.predict(scaled_features))
                raw_score = (self.model.decision_function(scaled_features)[0])
                anomaly = (prediction[0] == -1)                
                # SOC-friendly score
                ai_score = round(float(np.clip((1 - raw_score) * 100,0,100)),2)
                risk_score = min(int(ai_score),100)     
                return {
                    "anomaly": anomaly,
                    "ai_score": ai_score,
                    "risk_score": risk_score
                }
        except Exception as e:
            logger.exception(
                f"[AI] Prediction failed: {e}"
            )
            return {
                "anomaly": False,
                "ai_score": 0.0,
                "risk_score": 0,
                "error": str(e)
            }
    # =====================================================
    # Health Check
    # =====================================================
    def health(self):
        return {
            "trained": self.is_trained,
            "model_exists": os.path.exists(
                MODEL_PATH
            ),
            "scaler_exists": os.path.exists(
                SCALER_PATH
            )
        }
# =========================================================
# Singleton Instance
# =========================================================
detector = AnomalyDetector()