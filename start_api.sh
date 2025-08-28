#!/bin/bash

# Quick API Start Script for Diabetes Readmission Prediction

echo "🚀 Starting Diabetes Readmission Prediction API..."
echo "================================================"

# Check if we're in the right directory
if [ ! -f "notebooks/app.py" ]; then
    echo "❌ Error: app.py not found in notebooks directory"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo "📁 Starting API from project root directory..."
echo "🌐 API will be available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "❤️  Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the API"
echo ""

# Start the API from root directory to ensure correct file paths
python notebooks/app.py
