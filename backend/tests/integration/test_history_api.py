import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestHistoryAPI(unittest.TestCase):
    def setUp(self):
        self.client_context = TestClient(app)
        self.client = self.client_context.__enter__()

    def tearDown(self):
        self.client_context.__exit__(None, None, None)

    def test_predict_and_query_history_cycle(self):
        # 1. Send a prediction request
        payload = {
            "N": 85.0,
            "P": 50.0,
            "K": 40.0,
            "temperature": 25.5,
            "humidity": 78.0,
            "ph": 6.8,
            "rainfall": 180.0
        }
        predict_response = self.client.post("/api/v1/predict", json=payload)
        self.assertEqual(predict_response.status_code, 200)
        predict_data = predict_response.json()
        expected_crop = predict_data["recommended_crop"]

        # 2. Query history to verify it was stored in the database
        history_response = self.client.get("/api/v1/history?limit=5")
        self.assertEqual(history_response.status_code, 200)
        history_data = history_response.json()

        self.assertGreater(history_data["total_records"], 0)
        self.assertGreater(len(history_data["records"]), 0)

        # The most recent record should match our prediction
        latest_record = history_data["records"][0]
        self.assertEqual(latest_record["recommended_crop"], expected_crop)
        self.assertIsNotNone(latest_record["crop_detail"])
        self.assertEqual(latest_record["crop_detail"]["nitrogen"], 85.0)
        self.assertEqual(latest_record["crop_detail"]["rainfall"], 180.0)

if __name__ == "__main__":
    unittest.main()
