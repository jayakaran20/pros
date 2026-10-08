import time
import unittest
from pathlib import Path
from app.ml.wrappers.model_wrapper import crop_model

PROJECT_ROOT = Path(__file__).resolve().parents[3]

class TestMLQualityAndLatency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure model is loaded
        model_path = str(PROJECT_ROOT / "ml_experiments" / "models" / "xgboost_crop_model.json")
        scaler_path = str(PROJECT_ROOT / "ml_experiments" / "models" / "preprocessing_data.pkl")
        crop_model.load_model(model_path, scaler_path)

    def test_model_determinism(self):
        """Verifies that identical inputs yield strictly identical predictions with zero random drift."""
        sample_input = {
            "N": 90.0,
            "P": 42.0,
            "K": 43.0,
            "temperature": 20.87,
            "humidity": 82.00,
            "ph": 6.50,
            "rainfall": 202.93
        }

        first_crop, first_conf = crop_model.predict(sample_input)

        # Run 10 times and assert exact equality
        for _ in range(10):
            crop, conf = crop_model.predict(sample_input)
            self.assertEqual(crop, first_crop)
            self.assertAlmostEqual(conf, first_conf, places=4)

    def test_inference_latency_benchmark(self):
        """Verifies that ML inference satisfies the production latency gate: P95 < 50ms."""
        sample_input = {
            "N": 80.0,
            "P": 50.0,
            "K": 40.0,
            "temperature": 25.0,
            "humidity": 70.0,
            "ph": 6.5,
            "rainfall": 150.0
        }

        # Warmup run
        crop_model.predict(sample_input)

        latencies_ms = []
        iterations = 50

        for _ in range(iterations):
            start = time.perf_counter()
            crop_model.predict(sample_input)
            duration_ms = (time.perf_counter() - start) * 1000.0
            latencies_ms.append(duration_ms)

        latencies_ms.sort()
        p95_index = int(0.95 * len(latencies_ms))
        p95_latency = latencies_ms[p95_index]
        avg_latency = sum(latencies_ms) / len(latencies_ms)

        print(f"\n[BENCHMARK] Average latency: {avg_latency:.2f}ms | P95 latency: {p95_latency:.2f}ms")

        # Performance gate: P95 latency must be under 50ms (typically < 2ms with XGBoost Booster!)
        self.assertLess(p95_latency, 50.0, f"P95 latency exceeded threshold: {p95_latency:.2f}ms")

    def test_numerical_boundaries(self):
        """Tests that boundary agricultural conditions don't cause NaN or crash."""
        boundary_inputs = [
            {"N": 0.0, "P": 0.0, "K": 0.0, "temperature": 0.0, "humidity": 10.0, "ph": 4.0, "rainfall": 10.0},
            {"N": 140.0, "P": 145.0, "K": 205.0, "temperature": 45.0, "humidity": 100.0, "ph": 9.5, "rainfall": 300.0}
        ]

        for inp in boundary_inputs:
            crop, conf = crop_model.predict(inp)
            self.assertIsInstance(crop, str)
            self.assertGreaterEqual(conf, 0.0)
            self.assertLessEqual(conf, 100.0)

if __name__ == "__main__":
    unittest.main()
