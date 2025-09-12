#!/bin/bash

# Google Cloud Run Deployment Script for Diabetes Readmission Prediction API
# This script automates the deployment process to Google Cloud Run

set -e  # Exit on any error

# Configuration
PROJECT_ID=${GCP_PROJECT_ID:-"your-project-id"}
SERVICE_NAME="diabetes-readmission-api"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists gcloud; then
        print_error "Google Cloud CLI (gcloud) is not installed. Please install it first."
        exit 1
    fi
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install it first."
        exit 1
    fi
    
    if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" = "your-project-id" ]; then
        print_error "Please set GCP_PROJECT_ID environment variable or update PROJECT_ID in this script."
        exit 1
    fi
    
    print_success "All prerequisites are met!"
}

# Authenticate with Google Cloud
authenticate_gcloud() {
    print_status "Authenticating with Google Cloud..."
    
    # Check if already authenticated
    if gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_success "Already authenticated with Google Cloud"
    else
        print_status "Please authenticate with Google Cloud..."
        gcloud auth login
    fi
    
    # Set the project
    gcloud config set project $PROJECT_ID
    
    # Enable required APIs
    print_status "Enabling required Google Cloud APIs..."
    gcloud services enable cloudbuild.googleapis.com
    gcloud services enable run.googleapis.com
    gcloud services enable containerregistry.googleapis.com
    
    print_success "Google Cloud authentication completed!"
}

# Build Docker image
build_docker_image() {
    print_status "Building Docker image..."
    
    # Build the image
    docker build -f Dockerfile.fastapi -t $IMAGE_NAME:latest .
    
    if [ $? -eq 0 ]; then
        print_success "Docker image built successfully!"
    else
        print_error "Docker image build failed!"
        exit 1
    fi
}

# Push image to Google Container Registry
push_image() {
    print_status "Pushing image to Google Container Registry..."
    
    # Configure Docker to use gcloud as a credential helper
    gcloud auth configure-docker
    
    # Push the image
    docker push $IMAGE_NAME:latest
    
    if [ $? -eq 0 ]; then
        print_success "Image pushed successfully!"
    else
        print_error "Image push failed!"
        exit 1
    fi
}

# Deploy to Cloud Run
deploy_to_cloud_run() {
    print_status "Deploying to Google Cloud Run..."
    
    # Deploy the service
    gcloud run deploy $SERVICE_NAME \
        --image $IMAGE_NAME:latest \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --memory 2Gi \
        --cpu 2 \
        --max-instances 10 \
        --min-instances 1 \
        --port 8000 \
        --timeout 300 \
        --concurrency 100 \
        --set-env-vars ENVIRONMENT=production,MODEL_PATH=/app/models/lightgbm_optimized.pkl,SCALER_PATH=/app/models/feature_scaler.pkl,FEATURE_NAMES_PATH=/app/models/feature_names.pkl
    
    if [ $? -eq 0 ]; then
        print_success "Deployment to Cloud Run completed!"
    else
        print_error "Deployment to Cloud Run failed!"
        exit 1
    fi
}

# Get service URL and test
test_deployment() {
    print_status "Testing deployment..."
    
    # Get the service URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')
    
    if [ -z "$SERVICE_URL" ]; then
        print_error "Could not get service URL!"
        exit 1
    fi
    
    print_success "Service deployed at: $SERVICE_URL"
    
    # Wait for service to be ready
    print_status "Waiting for service to be ready..."
    sleep 30
    
    # Test health endpoint
    print_status "Testing health endpoint..."
    if curl -f "$SERVICE_URL/health" > /dev/null 2>&1; then
        print_success "Health check passed!"
    else
        print_warning "Health check failed, but service might still be starting up..."
    fi
    
    # Test prediction endpoint
    print_status "Testing prediction endpoint..."
    PREDICTION_RESPONSE=$(curl -s -X POST "$SERVICE_URL/predict" \
        -H "Content-Type: application/json" \
        -d '{
            "time_in_hospital": 5,
            "num_medications": 10,
            "number_diagnoses": 3,
            "age": "[50-60)"
        }')
    
    if echo "$PREDICTION_RESPONSE" | grep -q "prediction"; then
        print_success "Prediction endpoint test passed!"
        echo "Sample response: $PREDICTION_RESPONSE"
    else
        print_warning "Prediction endpoint test failed, but service might still be starting up..."
    fi
    
    print_success "Deployment completed successfully!"
    print_status "Service URL: $SERVICE_URL"
    print_status "API Documentation: $SERVICE_URL/docs"
    print_status "Health Check: $SERVICE_URL/health"
}

# Cleanup function
cleanup() {
    print_status "Cleaning up local Docker images..."
    docker rmi $IMAGE_NAME:latest 2>/dev/null || true
    print_success "Cleanup completed!"
}

# Main deployment function
main() {
    echo "=========================================="
    echo "Diabetes Readmission Prediction API"
    echo "Google Cloud Run Deployment Script"
    echo "=========================================="
    echo
    
    check_prerequisites
    authenticate_gcloud
    build_docker_image
    push_image
    deploy_to_cloud_run
    test_deployment
    cleanup
    
    echo
    echo "=========================================="
    print_success "Deployment completed successfully!"
    echo "=========================================="
}

# Run main function
main "$@"