#!/bin/bash

# ML API Deployment Script
# This script automates the deployment of the Diabetic Readmission ML API

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="diabetic-readmission-api"
CONTAINER_NAME="diabetic-readmission-api"
PORT=8000
NETWORK_NAME="ml-network"

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

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if port is available
check_port() {
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port $PORT is already in use. Stopping existing container..."
        docker stop $CONTAINER_NAME 2>/dev/null || true
        docker rm $CONTAINER_NAME 2>/dev/null || true
        sleep 2
    fi
}

# Function to build Docker image
build_image() {
    print_status "Building Docker image..."
    docker build -t $IMAGE_NAME:latest .
    print_success "Docker image built successfully"
}

# Function to create network if it doesn't exist
create_network() {
    if ! docker network ls | grep -q $NETWORK_NAME; then
        print_status "Creating Docker network: $NETWORK_NAME"
        docker network create $NETWORK_NAME
        print_success "Network created"
    else
        print_status "Network $NETWORK_NAME already exists"
    fi
}

# Function to run container
run_container() {
    print_status "Starting ML API container..."

    docker run -d \
        --name $CONTAINER_NAME \
        --network $NETWORK_NAME \
        -p $PORT:$PORT \
        -v $(pwd)/models:/app/models:ro \
        -v $(pwd)/feature_scaler.pkl:/app/feature_scaler.pkl:ro \
        -v $(pwd)/logs:/app/logs \
        --restart unless-stopped \
        --health-cmd="curl -f http://localhost:$PORT/health || exit 1" \
        --health-interval=30s \
        --health-timeout=10s \
        --health-retries=3 \
        $IMAGE_NAME:latest

    print_success "Container started successfully"
}

# Function to check container health
check_health() {
    print_status "Waiting for API to be ready..."

    # Wait for container to start
    sleep 5

    # Check container status
    if docker ps | grep -q $CONTAINER_NAME; then
        print_success "Container is running"
    else
        print_error "Container failed to start"
        docker logs $CONTAINER_NAME
        exit 1
    fi

    # Wait for API to be ready
    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:$PORT/health > /dev/null 2>&1; then
            print_success "API is ready and responding"
            break
        fi

        print_status "Waiting for API... (attempt $attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done

    if [ $attempt -gt $max_attempts ]; then
        print_error "API failed to become ready after $max_attempts attempts"
        docker logs $CONTAINER_NAME
        exit 1
    fi
}

# Function to show API information
show_api_info() {
    print_success "ML API Deployment Complete!"
    echo
    echo "🌐 API Endpoints:"
    echo "   • Main API: http://localhost:$PORT"
    echo "   • Health Check: http://localhost:$PORT/health"
    echo "   • API Documentation: http://localhost:$PORT/docs"
    echo "   • Model Information: http://localhost:$PORT/models"
    echo
    echo "📊 Container Status:"
    docker ps --filter name=$CONTAINER_NAME --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo
    echo "📝 Container Logs:"
    echo "   docker logs $CONTAINER_NAME"
    echo
    echo "🛑 Stop API:"
    echo "   docker stop $CONTAINER_NAME"
    echo
    echo "🚀 Restart API:"
    echo "   docker restart $CONTAINER_NAME"
}

# Function to test API
test_api() {
    print_status "Testing API endpoints..."

    # Test health endpoint
    if curl -s http://localhost:$PORT/health | grep -q "healthy"; then
        print_success "Health endpoint working"
    else
        print_error "Health endpoint failed"
    fi

    # Test models endpoint
    if curl -s http://localhost:$PORT/models > /dev/null; then
        print_success "Models endpoint working"
    else
        print_error "Models endpoint failed"
    fi

    # Test prediction endpoint with sample data
    sample_data='{"num_medications": 5, "time_in_hospital": 7, "number_diagnoses": 3, "num_procedures": 1, "num_lab_procedures": 25}'
    if curl -s -X POST http://localhost:$PORT/predict \
        -H "Content-Type: application/json" \
        -d "$sample_data" > /dev/null; then
        print_success "Prediction endpoint working"
    else
        print_error "Prediction endpoint failed"
    fi
}

# Main deployment function
deploy() {
    print_status "Starting ML API deployment..."
    echo

    check_docker
    check_port
    build_image
    create_network
    run_container
    check_health
    test_api
    show_api_info
}

# Function to stop and remove container
cleanup() {
    print_status "Cleaning up..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
    print_success "Cleanup completed"
}

# Function to show logs
logs() {
    if docker ps | grep -q $CONTAINER_NAME; then
        docker logs -f $CONTAINER_NAME
    else
        print_error "Container is not running"
    fi
}

# Function to show status
status() {
    if docker ps | grep -q $CONTAINER_NAME; then
        print_success "Container is running"
        docker ps --filter name=$CONTAINER_NAME --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    else
        print_warning "Container is not running"
    fi
}

# Main script logic
case "${1:-deploy}" in
    "deploy")
        deploy
        ;;
    "cleanup")
        cleanup
        ;;
    "logs")
        logs
        ;;
    "status")
        status
        ;;
    "restart")
        cleanup
        deploy
        ;;
    *)
        echo "Usage: $0 {deploy|cleanup|logs|status|restart}"
        echo
        echo "Commands:"
        echo "  deploy   - Deploy the ML API (default)"
        echo "  cleanup  - Stop and remove the container"
        echo "  logs     - Show container logs"
        echo "  status   - Show container status"
        echo "  restart  - Restart the API"
        exit 1
        ;;
esac
