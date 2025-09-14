#!/usr/bin/env python3
"""
Test script to verify API connection from Streamlit app context
"""
import requests
import os

# Test API connection
API_URL = "http://localhost:8000"

def test_api_connection():
    print("🔍 Testing API Connection...")
    print(f"API URL: {API_URL}")
    
    try:
        # Test health endpoint
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"Health Check Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API is working!")
            print(f"Status: {data['status']}")
            print(f"Model Loaded: {data['model_loaded']}")
            print(f"Model Performance: {data['model_performance']}")
            
            # Test prediction endpoint
            test_data = {
                "time_in_hospital": 5,
                "num_medications": 10,
                "number_diagnoses": 3,
                "age": "[50-60)"
            }
            
            pred_response = requests.post(f"{API_URL}/predict", json=test_data, timeout=10)
            print(f"Prediction Status: {pred_response.status_code}")
            
            if pred_response.status_code == 200:
                pred_data = pred_response.json()
                print("✅ Prediction is working!")
                print(f"Prediction: {pred_data['prediction']}")
                print(f"Probability: {pred_data['probability']:.4f}")
                print(f"Risk Level: {pred_data['risk_level']}")
            else:
                print("❌ Prediction failed")
                
        else:
            print("❌ API health check failed")
            
    except Exception as e:
        print(f"❌ API Error: {e}")

if __name__ == "__main__":
    test_api_connection()