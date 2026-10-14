# Model Card — Crop Recommendation XGBoost Engine

## 1. Model Details
* **Model Name**: Cropfit Crop Recommendation Model
* **Model Type**: Extreme Gradient Boosting (XGBoost) Classifier
* **Version**: 1.0.0
* **Serialization Format**: Native C++ XGBoost Booster JSON (`xgboost_crop_model.json`) with Z-score feature scaling parameters (`preprocessing_data.pkl`).
* **Developer**: Jayakaran (`jayakaran546@gmail.com`)
* **License**: MIT

---

## 2. Intended Use
* **Primary Intended Use**: Recommending optimal agricultural crops for farmers, agronomists, and agricultural extension workers based on localized soil chemical composition and microclimate data.
* **Out-of-Scope Use Cases**:
  - Financial crop market speculation without local soil testing.
  - Highly arid or arctic permafrost agricultural prediction without localized recalibration.

---

## 3. Input Features & Preprocessing

The model requires 7 continuous numerical features:

| Feature | Units | Valid Range | Description |
|---------|-------|-------------|-------------|
| `N` | Ratio | $\ge 0.0$ | Nitrogen content ratio in soil |
| `P` | Ratio | $\ge 0.0$ | Phosphorus content ratio in soil |
| `K` | Ratio | $\ge 0.0$ | Potassium content ratio in soil |
| `temperature` | °C | $-10.0$ to $60.0$ | Ambient temperature |
| `humidity` | % | $0.0$ to $100.0$ | Relative atmospheric humidity |
| `ph` | pH | $0.0$ to $14.0$ | Soil acidity/alkalinity scale |
| `rainfall` | mm | $\ge 0.0$ | Annual / seasonal precipitation |

* **Standardization**: Features are standardized using standard score transformation:
  $$z = \frac{x - \mu}{\sigma}$$
  where $\mu$ and $\sigma$ were computed during Phase 5 preprocessing.

---

## 4. Training Data & Methodology
* **Dataset**: Agronomic soil composition and crop suitability dataset (2,200 samples across 22 distinct crop classes).
* **Train / Validation / Test Split**: 70% Training (1,540 samples), 15% Validation (330 samples), 15% Test (330 samples).
* **Algorithm**: `xgboost.XGBClassifier` with `multi:softprob` objective and `mlogloss` evaluation metric.
* **Hyperparameters**:
  - `max_depth`: 4
  - `learning_rate`: 0.1
  - `n_estimators`: 100
  - `subsample`: 0.8
  - `colsample_bytree`: 0.8

---

## 5. Performance Metrics & Benchmarks

| Metric | Training Set | Validation Set | Test Set | SLA Target |
|--------|--------------|----------------|----------|------------|
| **Accuracy** | 99.4% | 88.5% | **88.18%** | $\ge 85.0\%$ |
| **Macro F1 Score** | 0.99 | 0.88 | **0.88** | $\ge 0.85$ |
| **P95 Latency** | $<2.0\text{ ms}$ | $<2.0\text{ ms}$ | **$1.8\text{ ms}$** | $<50.0\text{ ms}$ |

---

## 6. Limitations & Bias Considerations
* **Regional Soil Variations**: The model assumes standard tropical/subtropical agronomic zones. Extreme soil salinity or trace micronutrient deficiencies (e.g., zinc, iron) are not modeled.
* **Climate Change Shifts**: Rainfall patterns are assumed stationary; extreme unexpected flooding or droughts should be verified with local meteorological bulletins.
