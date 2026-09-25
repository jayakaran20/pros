# Machine Learning Experimentation (`ml_experiments/`)

This directory is dedicated exclusively to **offline data science, exploratory data analysis, and model training pipelines**.

## Architecture Boundary Rule

```
[ ml_experiments/ ]                  [ backend/app/ ]
Offline Data Science Work            Online Production Serving
- Raw datasets (data/raw/)           - Stateless FastAPI routes
- Jupyter Notebooks (notebooks/)     - Lightweight Inference Engines
- Training loops (src/train_*.py)    - Serialized artifacts only (.joblib / .pth)
- Hyperparameter search              - ZERO training code
```

### Subdirectories:
- `data/raw/`: Untouched original datasets (`.csv`, images). Ignored by Git.
- `data/processed/`: Scaled, split, and cleaned data arrays. Ignored by Git.
- `notebooks/`: Numbered exploratory Jupyter notebooks (`01_crop_eda.ipynb`, etc.).
- `src/`: Modular, reusable Python scripts for data loading, transformations, and model fitting.
- `saved_models/`: Local experiment checkpoints and weights before production promotion.
