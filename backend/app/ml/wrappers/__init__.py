"""
ML Inference Engine Wrappers.

Classes:
- `TabularEngine`: Handles tabular models (Scikit-learn, XGBoost) and preprocessing scalers.
- `VisionEngine`: Handles deep learning computer vision models (PyTorch MobileNetV3).

Rules:
- NO training loops or dataset downloads here. Strictly inference execution and tensor mapping.
"""
