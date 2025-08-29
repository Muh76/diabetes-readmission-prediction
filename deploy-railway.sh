#!/bin/bash

# Railway Deployment Script for Diabetes Readmission Prediction
# This script helps you deploy both FastAPI and Streamlit services on Railway

set -e

echo "🚀 Railway Deployment Script for Diabetes Readmission Prediction"
echo "================================================================"

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

# Check if required files exist
check_prerequisites() {
    print_status "Checking prerequisites..."

    local missing_files=()

    # Check Dockerfiles
    if [[ ! -f "Dockerfile.fastapi" ]]; then
        missing_files+=("Dockerfile.fastapi")
    fi

    if [[ ! -f "Dockerfile.streamlit" ]]; then
        missing_files+=("Dockerfile.streamlit")
    fi

    # Check requirements files
    if [[ ! -f "requirements-railway.txt" ]]; then
        missing_files+=("requirements-railway.txt")
    fi

    if [[ ! -f "requirements-streamlit.txt" ]]; then
        missing_files+=("requirements-streamlit.txt")
    fi

    # Check application files
    if [[ ! -f "notebooks/app.py" ]]; then
        missing_files+=("notebooks/app.py")
    fi

    if [[ ! -f "streamlit_app.py" ]]; then
        missing_files+=("streamlit_app.py")
    fi

    # Check model files
    if [[ ! -f "models/logistic_regression.pkl" ]]; then
        missing_files+=("models/logistic_regression.pkl")
    fi

    if [[ ! -f "feature_scaler.pkl" ]]; then
        missing_files+=("feature_scaler.pkl")
    fi

    if [[ ${#missing_files[@]} -gt 0 ]]; then
        print_error "Missing required files:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        exit 1
    fi

    print_success "All required files found!"
}

# Check if git is configured
check_git() {
    print_status "Checking Git configuration..."

    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not a Git repository. Please initialize Git first."
        exit 1
    fi

    if [[ -z "$(git config user.name)" ]] || [[ -z "$(git config user.email)" ]]; then
        print_warning "Git user.name or user.email not configured."
        print_status "Please run:"
        echo "  git config --global user.name 'Your Name'"
        echo "  git config --global user.email 'your.email@example.com'"
    fi

    print_success "Git repository configured!"
}

# Check if Railway CLI is installed
check_railway_cli() {
    print_status "Checking Railway CLI..."

    if ! command -v railway &> /dev/null; then
        print_warning "Railway CLI not found. Installing..."

        if command -v npm &> /dev/null; then
            npm install -g @railway/cli
        elif command -v yarn &> /dev/null; then
            yarn global add @railway/cli
        else
            print_error "npm or yarn not found. Please install Node.js first."
            print_status "Download from: https://nodejs.org/"
            exit 1
        fi
    fi

    print_success "Railway CLI found!"
}

# Build and test Docker images locally
test_docker_builds() {
    print_status "Testing Docker builds locally..."

    # Test FastAPI build
    print_status "Building FastAPI Docker image..."
    if docker build -f Dockerfile.fastapi -t diabetes-api-test .; then
        print_success "FastAPI Docker build successful!"
    else
        print_error "FastAPI Docker build failed!"
        exit 1
    fi

    # Test Streamlit build
    print_status "Building Streamlit Docker image..."
    if docker build -f Dockerfile.streamlit -t diabetes-streamlit-test .; then
        print_success "Streamlit Docker build successful!"
    else
        print_error "Streamlit Docker build failed!"
        exit 1
    fi

    # Clean up test images
    docker rmi diabetes-api-test diabetes-streamlit-test > /dev/null 2>&1 || true
}

# Deploy to Railway
deploy_to_railway() {
    print_status "Starting Railway deployment..."

    # Check if user is logged in to Railway
    if ! railway whoami &> /dev/null; then
        print_status "Please log in to Railway first..."
        railway login
    fi

    print_status "Creating new Railway project..."

    # Create new project
    local project_name="diabetes-readmission-prediction"
    local project_id=$(railway project create --name "$project_name" --json | jq -r '.id')

    if [[ -z "$project_id" ]] || [[ "$project_id" == "null" ]]; then
        print_error "Failed to create Railway project"
        exit 1
    fi

    print_success "Created Railway project: $project_name (ID: $project_id)"

    # Deploy FastAPI service
    print_status "Deploying FastAPI service..."
    railway service create --project "$project_id" --name "diabetes-api-fastapi" --dockerfile "Dockerfile.fastapi"

    # Deploy Streamlit service
    print_status "Deploying Streamlit service..."
    railway service create --project "$project_id" --name "diabetes-dashboard-streamlit" --dockerfile "Dockerfile.streamlit"

    print_success "Services created! Railway will now build and deploy them."
    print_status "Check the Railway dashboard for deployment progress:"
    echo "  https://railway.app/dashboard"
}

# Main deployment flow
main() {
    echo
    print_status "Starting deployment process..."

    # Check prerequisites
    check_prerequisites

    # Check Git configuration
    check_git

    # Check Railway CLI
    check_railway_cli

    # Test Docker builds
    test_docker_builds

    # Deploy to Railway
    deploy_to_railway

    echo
    print_success "Deployment process completed!"
    echo
    print_status "Next steps:"
    echo "  1. Wait for Railway to build and deploy your services"
    echo "  2. Check the Railway dashboard for deployment status"
    echo "  3. Test your endpoints once deployed"
    echo "  4. Configure custom domains if needed"
    echo
    print_status "Your services will be available at:"
    echo "  - FastAPI: https://diabetes-api-fastapi-production.up.railway.app"
    echo "  - Streamlit: https://diabetes-dashboard-streamlit-production.up.railway.app"
    echo
}

# Check if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
