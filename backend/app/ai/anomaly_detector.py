from sklearn.ensemble import IsolationForest
import numpy as np
import joblib
import os

MODEL_PATH = "ml_models/isolation_forest.pkl"

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(
            contamination=0.05,
            random_state=42
        )
        self.is_trained = False
    def train(self):
        training_data = []
        for _ in range(1000):
            src_port = np.random.randint(1024, 65535)
            dst_port = np.random.choice([
                80,
                443,
                53,
                22
            ])

            protocol = np.random.choice([1, 2])
            packet_count = np.random.randint(1, 20)
            training_data.append([
                src_port,
                dst_port,
                protocol,
                packet_count
            ])

        training_data = np.array(training_data)
        self.model.fit(training_data)
        self.is_trained = True
        os.makedirs("ml_models", exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)
        print("[AI] Model trained and saved.")

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.is_trained = True
            print("[AI] Model loaded.")
        else:
            self.train()

    def predict(self, features):

        if not self.is_trained:
            self.load_model()

        prediction = self.model.predict([features])
        score = self.model.decision_function([features])
        return {
            "anomaly": prediction[0] == -1,
            "score": float(score[0])
        }
detector = AnomalyDetector()