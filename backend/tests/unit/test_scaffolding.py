"""
Unit tests verifying application metadata and OpenAPI documentation status.
"""
import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestScaffolding(unittest.TestCase):
    def setUp(self):
        self.client_context = TestClient(app)
        self.client = self.client_context.__enter__()

    def tearDown(self):
        self.client_context.__exit__(None, None, None)

    def test_application_metadata(self):
        self.assertEqual(app.title, "Cropfit AI API")
        self.assertEqual(app.version, "2.0.0")

    def test_openapi_docs_accessible(self):
        response = self.client.get("/docs")
        self.assertEqual(response.status_code, 200)

    def test_openapi_json_schema(self):
        response = self.client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        paths = data["paths"]
        self.assertIn("/", paths)
        self.assertIn("/api/v1/predict", paths)
        self.assertIn("/api/v1/history", paths)
        self.assertIn("/api/v1/diseases/diagnose", paths)

if __name__ == "__main__":
    unittest.main()
