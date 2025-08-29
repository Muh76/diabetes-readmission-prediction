#!/usr/bin/env python3
"""
Railway Deployment Test Script
Tests both FastAPI and Streamlit services after deployment
"""

import sys
from urllib.parse import urljoin

import requests


def test_fastapi_service(base_url):
    """Test FastAPI service endpoints"""
    print(f"🔍 Testing FastAPI service at: {base_url}")

    # Test health endpoint
    try:
        health_url = urljoin(base_url, "/health")
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

    # Test API documentation
    try:
        docs_url = urljoin(base_url, "/docs")
        response = requests.get(docs_url, timeout=10)
        if response.status_code == 200:
            print("✅ API documentation accessible")
        else:
            print(f"❌ API documentation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API documentation error: {e}")

    # Test prediction endpoint with sample data
    try:
        predict_url = urljoin(base_url, "/predict")
        sample_data = {
            "encounter_id": 12345,
            "patient_nbr": 67890,
            "admission_type_id": 1,
            "discharge_disposition_id": 1,
            "admission_source_id": 1,
            "time_in_hospital": 5,
            "num_lab_procedures": 25,
            "num_procedures": 2,
            "num_medications": 8,
            "number_outpatient": 0,
            "number_emergency": 0,
            "number_inpatient": 1,
            "number_diagnoses": 5,
            "age_midpoint": 65,
            "service_utilization_score": 3,
            "clinical_risk_score": 4,
        }

        response = requests.post(predict_url, json=sample_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction endpoint working")
            print(f"   Prediction: {result.get('prediction', 'N/A')}")
            print(f"   Confidence: {result.get('confidence', 'N/A')}")
        else:
            print(f"❌ Prediction endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Prediction endpoint error: {e}")

    return True


def test_streamlit_service(base_url):
    """Test Streamlit service"""
    print(f"🔍 Testing Streamlit service at: {base_url}")

    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Streamlit dashboard accessible")
            if "Diabetes Readmission Prediction Dashboard" in response.text:
                print("✅ Dashboard content loaded correctly")
            else:
                print("⚠️  Dashboard content may not be fully loaded")
        else:
            print(f"❌ Streamlit service failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Streamlit service error: {e}")
        return False

    return True


def main():
    """Main test function"""
    print("🚀 Railway Deployment Test Script")
    print("==================================")

    # Get service URLs from user
    print("\nPlease enter your Railway service URLs:")

    fastapi_url = input(
        "FastAPI URL (e.g., https://diabetes-api-fastapi-production.up.railway.app): "
    ).strip()
    if not fastapi_url:
        print("❌ FastAPI URL is required")
        sys.exit(1)

    streamlit_url = input(
        "Streamlit URL (e.g., https://diabetes-dashboard-streamlit-production.up.railway.app): "
    ).strip()
    if not streamlit_url:
        print("❌ Streamlit URL is required")
        sys.exit(1)

    print("\n" + "=" * 50)

    # Test services
    fastapi_success = test_fastapi_service(fastapi_url)
    print()
    streamlit_success = test_streamlit_service(streamlit_url)

    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)

    if fastapi_success:
        print("✅ FastAPI Service: PASSED")
    else:
        print("❌ FastAPI Service: FAILED")

    if streamlit_success:
        print("✅ Streamlit Service: PASSED")
    else:
        print("❌ Streamlit Service: FAILED")

    if fastapi_success and streamlit_success:
        print("\n🎉 All services are working correctly!")
        print("\nYour deployment is successful! 🚀")
        print(f"FastAPI: {fastapi_url}")
        print(f"Streamlit: {streamlit_url}")
    else:
        print("\n⚠️  Some services have issues. Check the logs above.")
        print("Check Railway dashboard for deployment status and logs.")


if __name__ == "__main__":
    main()
