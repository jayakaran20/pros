"""
Cropfit Production Smoke Test Script
------------------------------------
Executes rapid automated verification of all core API endpoints,
Machine Learning models, database persistence, and computer vision diagnosis.
Can be executed against local development, Docker containers, or live cloud URLs.

Usage:
    python backend/scripts/smoke_test.py
    python backend/scripts/smoke_test.py --base-url https://cropfit-backend.onrender.com
"""

import sys
import io
import time
import argparse
from typing import Dict, Any

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import httpx
from PIL import Image

def run_smoke_tests(base_url: str):
    base_url = base_url.rstrip("/")
    print(f"\n[START] Cropfit Production Smoke Tests against: {base_url}")
    print("=" * 65)
    
    start_total_time = time.time()
    tests_passed = 0
    total_tests = 4

    client = httpx.Client(base_url=base_url, timeout=15.0)

    # -------------------------------------------------------------------------
    # TEST 1: Health & Readiness Probe
    # -------------------------------------------------------------------------
    print("[1/4] Probing Service Health & Readiness Probe (/api/v1/health)...")
    t0 = time.time()
    try:
        health_resp = client.get("/api/v1/health")
        t_health = (time.time() - t0) * 1000
        assert health_resp.status_code == 200, f"Expected status 200, got {health_resp.status_code}"
        health_data = health_resp.json()
        assert health_data.get("status") == "healthy", f"Status not healthy: {health_data}"
        assert health_data.get("crop_model_loaded") is True, "XGBoost Crop Model not loaded"
        assert health_data.get("vision_engine_loaded") is True, "Computer Vision Engine not loaded"
        print(f"      [PASS] Backend healthy | Models Resident in Memory ({t_health:.1f}ms)")
        tests_passed += 1
    except Exception as e:
        print(f"      [FAIL] Health probe failed: {e}")

    # -------------------------------------------------------------------------
    # TEST 2: Crop Recommendation Inference
    # -------------------------------------------------------------------------
    print("[2/4] Testing ML Crop Recommendation Endpoint (/api/v1/predict)...")
    payload = {
        "N": 90.0,
        "P": 42.0,
        "K": 43.0,
        "temperature": 20.87,
        "humidity": 82.00,
        "ph": 6.50,
        "rainfall": 202.93
    }
    t0 = time.time()
    try:
        pred_resp = client.post("/api/v1/predict", json=payload)
        t_pred = (time.time() - t0) * 1000
        assert pred_resp.status_code == 200, f"Expected status 200, got {pred_resp.status_code}"
        pred_data = pred_resp.json()
        crop = pred_data.get("recommended_crop")
        conf = pred_data.get("confidence_score")
        assert crop is not None and len(crop) > 0, "No recommended crop returned"
        assert conf is not None and 0.0 <= conf <= 100.0, f"Confidence score out of bounds (0-100): {conf}"
        print(f"      [PASS] Recommended '{crop}' with {conf:.1f}% confidence ({t_pred:.1f}ms)")
        tests_passed += 1
    except Exception as e:
        print(f"      [FAIL] Crop recommendation failed: {e}")

    # -------------------------------------------------------------------------
    # TEST 3: Prediction Audit Trail & Database Query
    # -------------------------------------------------------------------------
    print("[3/4] Testing Database History Audit (/api/v1/history)...")
    t0 = time.time()
    try:
        hist_resp = client.get("/api/v1/history?limit=5")
        t_hist = (time.time() - t0) * 1000
        assert hist_resp.status_code == 200, f"Expected status 200, got {hist_resp.status_code}"
        hist_data = hist_resp.json()
        records = hist_data.get("records", [])
        assert len(records) > 0, "Expected at least 1 record in database history"
        print(f"      [PASS] Retrieved {len(records)} audit records | Total: {hist_data.get('total_records')} ({t_hist:.1f}ms)")
        tests_passed += 1
    except Exception as e:
        print(f"      [FAIL] Database history audit failed: {e}")

    # -------------------------------------------------------------------------
    # TEST 4: Computer Vision Disease Diagnosis Upload
    # -------------------------------------------------------------------------
    print("[4/4] Testing Computer Vision Plant Disease Diagnosis (/api/v1/diseases/diagnose)...")
    # Generate an in-memory sample RGB leaf image (100x100 green patch)
    img_byte_arr = io.BytesIO()
    test_image = Image.new("RGB", (100, 100), color=(45, 130, 45))
    test_image.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)

    t0 = time.time()
    try:
        files = {"file": ("test_leaf.jpg", img_byte_arr.getvalue(), "image/jpeg")}
        disease_resp = client.post("/api/v1/diseases/diagnose", files=files)
        t_disease = (time.time() - t0) * 1000
        assert disease_resp.status_code == 200, f"Expected status 200, got {disease_resp.status_code}"
        disease_data = disease_resp.json()
        crop_name = disease_data.get("crop")
        condition = disease_data.get("condition")
        conf = disease_data.get("confidence_score")
        treatments = disease_data.get("treatment_recommendations", [])
        assert condition is not None, "Missing condition in diagnosis"
        assert conf is not None and 0.0 <= conf <= 100.0, f"Confidence score out of range: {conf}"
        assert len(treatments) > 0, "Missing treatment recommendations"
        print(f"      [PASS] Diagnosed '{crop_name} - {condition}' ({conf:.1f}%) | {len(treatments)} treatments ({t_disease:.1f}ms)")
        tests_passed += 1
    except Exception as e:
        print(f"      [FAIL] Disease diagnosis failed: {e}")

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    total_time = (time.time() - start_total_time) * 1000
    print("=" * 65)
    print(f"[SUMMARY] Smoke Test Results: {tests_passed}/{total_tests} passed in {total_time:.1f}ms")
    
    if tests_passed == total_tests:
        print("[SUCCESS] ALL PRODUCTION SMOKE TESTS PASSED! System is 100% operational.")
        return 0
    else:
        print(f"[ERROR] {total_tests - tests_passed} test(s) failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cropfit Production Smoke Test Suite")
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="Target base URL of the Cropfit API (default: http://127.0.0.1:8000)",
    )
    args = parser.parse_args()
    sys.exit(run_smoke_tests(args.base_url))
