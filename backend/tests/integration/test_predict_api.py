import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestPredictAPI(unittest.TestCase):
    def setUp(self):
        # Using context manager to trigger lifespan startup (which loads the ML model)
        self.client_context = TestClient(app)
        self.client = self.client_context.__enter__()

    def tearDown(self):
        self.client_context.__exit__(None, None, None)

    def test_health_check(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_predict_crop_valid_data(self):
        payload = {
            "N": 90.0,
            "P": 42.0,
            "K": 43.0,
            "temperature": 20.87,
            "humidity": 82.00,
            "ph": 6.50,
            "rainfall": 202.93
        }
        response = self.client.post("/api/v1/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("recommended_crop", data)
        self.assertIn("confidence_score", data)
        self.assertIsInstance(data["recommended_crop"], str)
        self.assertGreater(data["confidence_score"], 0.0)

    def test_predict_crop_invalid_data(self):
        # Missing required 'rainfall' field
        invalid_payload = {
            "N": 90.0,
            "P": 42.0,
            "K": 43.0,
            "temperature": 20.87,
            "humidity": 82.00,
            "ph": 6.50
        }
        response = self.client.post("/api/v1/predict", json=invalid_payload)
        # Should be rejected by Pydantic validation with 422 Unprocessable Entity
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()
