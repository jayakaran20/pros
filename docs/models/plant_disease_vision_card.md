# Model Card — Plant Leaf Disease Computer Vision Engine

## 1. Model Details
* **Model Name**: Cropfit Plant Disease Diagnostic Vision Engine
* **Model Architecture**: MobileNetV3-Small backbone with fine-tuned botanical classification head.
* **Inference Runtime**: ONNX Runtime (`mobilenet_disease.onnx`) with colorimetric/texture fallback heuristics.
* **Knowledge Base**: Curated botanical agronomy database (`disease_classes.json`).
* **Developer**: Jayakaran (`jayakaran546@gmail.com`)
* **License**: MIT

---

## 2. Intended Use
* **Primary Intended Use**: Early-stage in-field identification of crop foliar pathologies (fungal, bacterial, viral, and environmental stress) from user-submitted mobile smartphone photos.
* **Out-of-Scope Use Cases**:
  - Root-knot nematode diagnosis (requires subterranean root sampling).
  - Microscopic spore identification without optical magnification.

---

## 3. Supported Botanical Categories (11 Classes)

1. **Tomato — Early Blight** (*Alternaria solani*)
2. **Tomato — Late Blight** (*Phytophthora infestans*)
3. **Tomato — Leaf Mold** (*Passalora fulva*)
4. **Tomato — Septoria Leaf Spot** (*Septoria lycopersici*)
5. **Tomato — Bacterial Spot** (*Xanthomonas*)
6. **Tomato — Healthy Foliage**
7. **Potato — Early Blight** (*Alternaria solani*)
8. **Potato — Late Blight** (*Phytophthora infestans*)
9. **Potato — Healthy Foliage**
10. **Pepper Bell — Bacterial Spot** (*Xanthomonas campestris*)
11. **Pepper Bell — Healthy Foliage**

---

## 4. Preprocessing Pipeline

1. **Resolution Normalization**: Input images are decoded via Pillow (PIL) and resized to $224 \times 224 \times 3$ RGB.
2. **Standardization**: Pixel values are normalized using ImageNet channel distributions:
   $$\mu = [0.485, 0.456, 0.406], \quad \sigma = [0.229, 0.224, 0.225]$$
3. **Tensor Ordering**: Transposed to channel-first format (`(1, 3, 224, 224)`) in single-precision floating point (`float32`).

---

## 5. Inference & SLA Benchmarks

* **Inference Latency**:
  - ONNX CPU Runtime: $\approx 15\text{ ms}$ to $25\text{ ms}$ per image.
  - Overall HTTP Cycle: $\approx 35\text{ ms}$ (including multipart parsing and payload generation).
* **Confidence Gating**:
  - Predictions with confidence $< 40\%$ prompt visual inspection or high-resolution re-capture warnings.

---

## 6. Recommendations & Actionable Guidance

Each diagnosed class is coupled with:
* **Risk Severity**: Low, Medium, or High.
* **Key Visual Symptoms**: Morphological indicators for verification.
* **Treatment Recommendations**: Both organic (e.g., *Bacillus subtilis*, copper fungicides, potassium bicarbonate) and chemical options.
* **Prevention Tips**: Drip irrigation, crop rotation, and sanitization protocols.
