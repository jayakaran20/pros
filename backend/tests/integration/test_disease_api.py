import io
import unittest
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

class TestDiseaseAPI(unittest.TestCase):
    def setUp(self):
        self.client_context = TestClient(app)
        self.client = self.client_context.__enter__()

    def tearDown(self):
        self.client_context.__exit__(None, None, None)

    def _create_test_image(self, color=(34, 139, 34)) -> io.BytesIO:
        """Creates an in-memory 224x224 RGB JPEG image for testing."""
        img = Image.new("RGB", (224, 224), color=color)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)
        return buf

    def test_diagnose_valid_image(self):
        img_buf = self._create_test_image(color=(34, 139, 34))
        files = {"file": ("test_leaf.jpg", img_buf, "image/jpeg")}
        
        response = self.client.post("/api/v1/diseases/diagnose", files=files)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("crop", data)
        self.assertIn("condition", data)
        self.assertIn("confidence_score", data)
        self.assertIn("severity", data)
        self.assertIn("symptoms", data)
        self.assertIn("treatment_recommendations", data)
        self.assertIsInstance(data["symptoms"], list)
        self.assertGreater(len(data["symptoms"]), 0)

    def test_reject_unsupported_file_type(self):
        text_file = io.BytesIO(b"Hello world, this is a plain text file, not a leaf photo.")
        files = {"file": ("notes.txt", text_file, "text/plain")}
        
        response = self.client.post("/api/v1/diseases/diagnose", files=files)
        # Should be rejected with 415 Unsupported Media Type
        self.assertEqual(response.status_code, 415)

    def test_reject_empty_file(self):
        empty_buf = io.BytesIO(b"")
        files = {"file": ("empty.jpg", empty_buf, "image/jpeg")}
        
        response = self.client.post("/api/v1/diseases/diagnose", files=files)
        self.assertEqual(response.status_code, 400)

    def test_disease_diagnosis_persists_to_database(self):
        # 1. Diagnose image
        img_buf = self._create_test_image(color=(50, 160, 40))
        files = {"file": ("field_leaf.jpg", img_buf, "image/jpeg")}
        diag_resp = self.client.post("/api/v1/diseases/diagnose", files=files)
        self.assertEqual(diag_resp.status_code, 200)

        # 2. Query history to confirm it was stored in SQLite with task_type='disease_detection'
        hist_resp = self.client.get("/api/v1/history?task_type=disease_detection&limit=5")
        self.assertEqual(hist_resp.status_code, 200)
        hist_data = hist_resp.json()
        
        self.assertGreater(hist_data["total_records"], 0)
        latest = hist_data["records"][0]
        self.assertEqual(latest["task_type"], "disease_detection")
        self.assertIn(diag_resp.json()["crop"], latest["recommended_crop"])

if __name__ == "__main__":
    unittest.main()
