"""
Sanity test verifying that the backend application package is importable
and metadata matches the architectural plan.
"""

import unittest

from backend.app.main import get_application_info


class TestScaffolding(unittest.TestCase):
    def test_application_scaffolding_metadata(self):
        info = get_application_info()
        self.assertEqual(info["title"], "Smart Crop Assistant API")
        self.assertEqual(info["version"], "0.1.0")
        self.assertEqual(info["status"], "scaffolded")


if __name__ == "__main__":
    unittest.main()
