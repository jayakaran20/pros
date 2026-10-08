import unittest
from pydantic import ValidationError
from app.schemas.crop import CropPredictionRequest, CropPredictionResponse
from app.schemas.disease import DiseaseDiagnosisResponse

class TestSchemas(unittest.TestCase):
    def test_valid_crop_request(self):
        req = CropPredictionRequest(
            N=90.0,
            P=42.0,
            K=43.0,
            temperature=20.8,
            humidity=82.0,
            ph=6.5,
            rainfall=202.9
        )
        self.assertEqual(req.N, 90.0)
        self.assertEqual(req.ph, 6.5)

    def test_reject_negative_nutrients(self):
        with self.assertRaises(ValidationError):
            CropPredictionRequest(
                N=-10.0,  # Invalid: ge=0.0
                P=42.0,
                K=43.0,
                temperature=20.8,
                humidity=82.0,
                ph=6.5,
                rainfall=202.9
            )

    def test_reject_invalid_ph(self):
        with self.assertRaises(ValidationError):
            CropPredictionRequest(
                N=90.0,
                P=42.0,
                K=43.0,
                temperature=20.8,
                humidity=82.0,
                ph=15.5,  # Invalid: le=14.0
                rainfall=202.9
            )

    def test_reject_invalid_humidity(self):
        with self.assertRaises(ValidationError):
            CropPredictionRequest(
                N=90.0,
                P=42.0,
                K=43.0,
                temperature=20.8,
                humidity=120.0,  # Invalid: le=100.0
                ph=6.5,
                rainfall=202.9
            )

    def test_valid_crop_response(self):
        res = CropPredictionResponse(
            recommended_crop="rice",
            confidence_score=94.5
        )
        self.assertEqual(res.recommended_crop, "rice")
        self.assertEqual(res.confidence_score, 94.5)

    def test_valid_disease_response(self):
        diag = DiseaseDiagnosisResponse(
            crop="Tomato",
            condition="Early Blight",
            is_healthy=False,
            confidence_score=91.2,
            severity="Medium",
            symptoms=["Concentric rings"],
            treatment_recommendations=["Copper fungicide"],
            prevention_tips=["Mulch base"]
        )
        self.assertEqual(diag.crop, "Tomato")
        self.assertFalse(diag.is_healthy)

if __name__ == "__main__":
    unittest.main()
