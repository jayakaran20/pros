# Session 004 — ML Pipeline Complete

## Status: 🟢 Completed (Approved 2026-09-30)

---

## Objective
Design, train, evaluate, and export a Machine Learning model capable of predicting the ideal crop based on environmental and soil conditions.

## Technical Pivots
- **Python 3.14 Compatibility Issue**: `scikit-learn` v1.9.1 exhibited Cython binary incompatibility (`KeyError: '__reduce_cython__'`) when using `train_test_split`.
- **Resolution**: Implemented manual stratification using `pandas` and bypassed sklearn modeling completely by pivoting to `xgboost.XGBClassifier`.

## Sub-sessions Completed

### 1. Data Preprocessing (S015 - S017)
- Encoded categorical text labels (22 crops) into numerical integers using dictionaries.
- Split data into an 80/20 train/test split.
- Scaled features (Standardization) to prevent features with naturally larger numbers (like rainfall) from overwhelming the algorithm. 
- *Critical rule enforced*: Fit the scaler strictly on the training set, not the test set, to prevent data leakage.

### 2. Modeling (S018 - S023)
- Bypassed Scikit-learn baselines due to Python 3.14 incompatibilities.
- Trained an `XGBoost` model using 100 decision trees (`n_estimators=100`).
- Model achieved a baseline accuracy of **88.18%** on the hold-out test set.

### 3. Evaluation (S024 - S026)
- **Feature Importance**: Generated an XGBoost feature importance chart.
  - **Humidity** and **Rainfall** are the most determinative factors for crop classification in this dataset.
  - Temperature and K (Potassium) had the lowest overall weight.
- **Confusion Matrix**: Generated a crosstab visualization to analyze per-class error distribution. The model demonstrates extremely high separability.

### 4. Export & Serialization (S027 - S029)
- Saved the trained mathematical model to `ml_experiments/models/xgboost_crop_model.json`.
- Saved the preprocessing parameters (Mean, Standard Deviation) and the Label Dictionary (Crop Map) to `ml_experiments/models/preprocessing_data.pkl` using the standard `pickle` library.
- The ML artifact is now strictly decoupled and ready to be loaded by the FastAPI backend inference engine.

## Verification & Version Control
- All Jupyter Notebooks (`04_preprocessing_and_baseline.ipynb`, `05_model_evaluation_and_export.ipynb`) committed.
- Exported models and pickles ignored from git if necessary, but scripts committed.
- Roadmap updated to mark S015-S029 as Completed.
