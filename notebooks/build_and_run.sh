#!/bin/bash

echo "🐳 Building Docker Image for ML Pipeline..."

# Build the image
docker build -t diabetic-readmission-ml .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo "🚀 Starting services with docker-compose..."

    # Start services
    docker-compose up -d

    echo "✅ Services started successfully!"
    echo "�� MLflow UI: http://localhost:5000"
    echo "🔌 API: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
else
    echo "❌ Docker build failed!"
    exit 1
fi
