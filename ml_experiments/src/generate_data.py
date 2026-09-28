import pandas as pd
import numpy as np
import os

output_path = "ml_experiments/data/raw/crop_recommendation.csv"

# The 22 standard crops from the original dataset
crops = [
    'rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
    'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate',
    'banana', 'mango', 'grapes', 'watermelon', 'muskmelon',
    'apple', 'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee'
]

# Random seed for reproducibility
np.random.seed(42)

data = []
samples_per_crop = 100  # Total 2200 rows, just like the original dataset

print("Generating realistic synthetic crop data...")

for crop in crops:
    # Generate realistic-looking random centers for each crop's requirements
    n_base = np.random.uniform(20, 100)
    p_base = np.random.uniform(20, 80)
    k_base = np.random.uniform(20, 60)
    temp_base = np.random.uniform(20, 35)
    hum_base = np.random.uniform(50, 90)
    ph_base = np.random.uniform(5.5, 7.5)
    rain_base = np.random.uniform(50, 200)

    for _ in range(samples_per_crop):
        # Add random noise around the base values
        data.append({
            'N': max(0, int(np.random.normal(n_base, 10))),
            'P': max(0, int(np.random.normal(p_base, 8))),
            'K': max(0, int(np.random.normal(k_base, 8))),
            'temperature': round(np.random.normal(temp_base, 3), 2),
            'humidity': round(np.random.normal(hum_base, 5), 2),
            'ph': round(np.random.normal(ph_base, 0.4), 2),
            'rainfall': round(np.random.normal(rain_base, 20), 2),
            'label': crop
        })

df = pd.DataFrame(data)

# Save to the raw data folder
df.to_csv(output_path, index=False)

print(f"✅ Success! Generated 2,200 rows and saved to {output_path}")
print(f"📊 Dataset Shape: {df.shape}")
