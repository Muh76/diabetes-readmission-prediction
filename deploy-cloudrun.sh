#!/bin/bash

# Google Cloud Run Deployment Script
echo "🚀 Deploying FastAPI to Google Cloud Run..."

# Set variables
PROJECT_ID="your-project-id"  # Replace with your project ID
SERVICE_NAME="diabetes-fastapi"
REGION="us-central1"

# Build and deploy
echo "📦 Building and deploying..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10

echo "✅ Deployment complete!"
echo "🌐 Your API URL: https://$SERVICE_NAME-$REGION.a.run.app"
echo "📚 API Docs: https://$SERVICE_NAME-$REGION.a.run.app/docs"
echo "❤️ Health Check: https://$SERVICE_NAME-$REGION.a.run.app/health"
