import pickle
import xgboost as xgb
import numpy as np
import os

class CropModelWrapper:
    _instance = None  # Singleton instance

    def __init__(self):
        self.booster = None
        self.mean = None
        self.std = None
        self.crop_map = None
        self.is_loaded = False
        self.feature_order = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_model(self, model_path: str, scaler_path: str):
        """Loads the native XGBoost Booster model and scaler into memory."""
        if self.is_loaded:
            return

        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Model files not found at {model_path} or {scaler_path}")

        # 1. Load native XGBoost Booster without any sklearn wrapper dependency
        self.booster = xgb.Booster()
        self.booster.load_model(model_path)

        # 2. Load the preprocessing values (mean, std, crop dictionary)
        with open(scaler_path, 'rb') as f:
            preprocessing_data = pickle.load(f)

        self.mean = preprocessing_data['mean']
        self.std = preprocessing_data['std']
        self.crop_map = preprocessing_data['crop_map']

        self.is_loaded = True
        print("[INFO] Native XGBoost Booster successfully loaded into memory!")

    def predict(self, input_data: dict) -> tuple[str, float]:
        """Runs the prediction using native XGBoost Booster DMatrix."""
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded yet!")

        # Standardize features in exact training order: (x - mean) / std
        scaled_features = [
            (float(input_data[f]) - float(self.mean[f])) / float(self.std[f])
            for f in self.feature_order
        ]

        # Construct DMatrix with exact feature names expected by the model
        input_array = np.array([scaled_features], dtype=np.float32)
        dmatrix = xgb.DMatrix(input_array, feature_names=self.feature_order)

        # Native predict returns probabilities across all 22 classes
        probabilities = self.booster.predict(dmatrix)[0]
        predicted_class_idx = int(np.argmax(probabilities))

        # Top probability percentage
        confidence = float(probabilities[predicted_class_idx]) * 100

        # Translate integer class back to crop name
        crop_name = self.crop_map[predicted_class_idx]

        return crop_name, confidence

# Export the singleton
crop_model = CropModelWrapper.get_instance()
