#!/bin/bash

# MLflow Server Startup Script for Diabetes Readmission Prediction Project
# This script starts MLflow tracking server with proper configuration

set -e  # Exit on any error

# Configuration
MLFLOW_HOST=${MLFLOW_HOST:-"0.0.0.0"}
MLFLOW_PORT=${MLFLOW_PORT:-"5000"}
MLFLOW_BACKEND_STORE_URI=${MLFLOW_BACKEND_STORE_URI:-"sqlite:///mlflow.db"}
MLFLOW_DEFAULT_ARTIFACT_ROOT=${MLFLOW_DEFAULT_ARTIFACT_ROOT:-"./mlflow_artifacts"}
MLFLOW_CONFIG_FILE=${MLFLOW_CONFIG_FILE:-"./mlflow.conf"}

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
    
    if ! command_exists mlflow; then
        print_error "MLflow is not installed. Please install it first:"
        echo "pip install mlflow"
        exit 1
    fi
    
    if ! command_exists python; then
        print_error "Python is not installed. Please install it first."
        exit 1
    fi
    
    print_success "All prerequisites are met!"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p "$MLFLOW_DEFAULT_ARTIFACT_ROOT"
    mkdir -p "./mlflow_logs"
    mkdir -p "./mlflow_backups"
    mkdir -p "./mlflow_exports"
    mkdir -p "./mlflow_docs"
    mkdir -p "./mlflow_packages"
    
    print_success "Directories created successfully!"
}

# Initialize MLflow database
init_database() {
    print_status "Initializing MLflow database..."
    
    if [ ! -f "mlflow.db" ]; then
        print_status "Creating new MLflow database..."
        # Create database by running a simple MLflow command
        python -c "
import mlflow
mlflow.set_tracking_uri('$MLFLOW_BACKEND_STORE_URI')
try:
    mlflow.create_experiment('diabetes-readmission-prediction')
    print('MLflow database initialized successfully')
except:
    print('MLflow database already exists')
"
    else
        print_success "MLflow database already exists"
    fi
}

# Start MLflow server
start_mlflow_server() {
    print_status "Starting MLflow tracking server..."
    
    # Check if MLflow server is already running
    if curl -s "http://$MLFLOW_HOST:$MLFLOW_PORT" > /dev/null 2>&1; then
        print_warning "MLflow server is already running at http://$MLFLOW_HOST:$MLFLOW_PORT"
        print_status "You can access it at: http://$MLFLOW_HOST:$MLFLOW_PORT"
        return 0
    fi
    
    # Start MLflow server
    print_status "Starting MLflow server with the following configuration:"
    echo "  Host: $MLFLOW_HOST"
    echo "  Port: $MLFLOW_PORT"
    echo "  Backend Store URI: $MLFLOW_BACKEND_STORE_URI"
    echo "  Artifact Root: $MLFLOW_DEFAULT_ARTIFACT_ROOT"
    echo "  Config File: $MLFLOW_CONFIG_FILE"
    echo
    
    # Start server in background
    nohup mlflow server \
        --host "$MLFLOW_HOST" \
        --port "$MLFLOW_PORT" \
        --backend-store-uri "$MLFLOW_BACKEND_STORE_URI" \
        --default-artifact-root "$MLFLOW_DEFAULT_ARTIFACT_ROOT" \
        --gunicorn-opts "--timeout 120" \
        > "./mlflow_logs/mlflow_server.log" 2>&1 &
    
    MLFLOW_PID=$!
    echo $MLFLOW_PID > "./mlflow_logs/mlflow_server.pid"
    
    # Wait for server to start
    print_status "Waiting for MLflow server to start..."
    sleep 10
    
    # Check if server is running
    if curl -s "http://$MLFLOW_HOST:$MLFLOW_PORT" > /dev/null 2>&1; then
        print_success "MLflow server started successfully!"
        print_status "Server PID: $MLFLOW_PID"
        print_status "Access MLflow UI at: http://$MLFLOW_HOST:$MLFLOW_PORT"
        print_status "Logs are available at: ./mlflow_logs/mlflow_server.log"
    else
        print_error "Failed to start MLflow server. Check logs at: ./mlflow_logs/mlflow_server.log"
        exit 1
    fi
}

# Test MLflow connection
test_mlflow_connection() {
    print_status "Testing MLflow connection..."
    
    python -c "
import mlflow
import requests
import time

# Set tracking URI
mlflow.set_tracking_uri('http://$MLFLOW_HOST:$MLFLOW_PORT')

# Test connection
try:
    # Test HTTP connection
    response = requests.get('http://$MLFLOW_HOST:$MLFLOW_PORT', timeout=10)
    if response.status_code == 200:
        print('✅ MLflow server is responding')
    else:
        print('❌ MLflow server returned status code:', response.status_code)
        exit(1)
    
    # Test MLflow client connection
    client = mlflow.tracking.MlflowClient()
    experiments = client.search_experiments()
    print('✅ MLflow client connection successful')
    print(f'Found {len(experiments)} experiments')
    
    # Test creating a run
    with mlflow.start_run(run_name='connection_test') as run:
        mlflow.log_param('test_param', 'test_value')
        mlflow.log_metric('test_metric', 0.95)
        print('✅ MLflow run creation successful')
        print(f'Run ID: {run.info.run_id}')
    
except Exception as e:
    print('❌ MLflow connection test failed:', str(e))
    exit(1)
"
    
    if [ $? -eq 0 ]; then
        print_success "MLflow connection test passed!"
    else
        print_error "MLflow connection test failed!"
        exit 1
    fi
}

# Log your pipeline results
log_pipeline_results() {
    print_status "Logging your pipeline results to MLflow..."
    
    python -c "
import sys
sys.path.append('.')
from mlflow_manager import log_your_pipeline_results

try:
    run_id = log_your_pipeline_results()
    print(f'✅ Pipeline results logged successfully with run ID: {run_id}')
except Exception as e:
    print(f'❌ Failed to log pipeline results: {str(e)}')
    exit(1)
"
    
    if [ $? -eq 0 ]; then
        print_success "Pipeline results logged successfully!"
    else
        print_error "Failed to log pipeline results!"
        exit 1
    fi
}

# Stop MLflow server
stop_mlflow_server() {
    print_status "Stopping MLflow server..."
    
    if [ -f "./mlflow_logs/mlflow_server.pid" ]; then
        PID=$(cat "./mlflow_logs/mlflow_server.pid")
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID"
            print_success "MLflow server stopped successfully!"
        else
            print_warning "MLflow server process not found"
        fi
        rm -f "./mlflow_logs/mlflow_server.pid"
    else
        print_warning "No PID file found. MLflow server may not be running."
    fi
}

# Show MLflow status
show_status() {
    print_status "MLflow Server Status:"
    echo
    
    if [ -f "./mlflow_logs/mlflow_server.pid" ]; then
        PID=$(cat "./mlflow_logs/mlflow_server.pid")
        if kill -0 "$PID" 2>/dev/null; then
            print_success "MLflow server is running (PID: $PID)"
            print_status "Access URL: http://$MLFLOW_HOST:$MLFLOW_PORT"
        else
            print_warning "MLflow server PID file exists but process is not running"
        fi
    else
        print_warning "MLflow server is not running"
    fi
    
    echo
    print_status "Configuration:"
    echo "  Host: $MLFLOW_HOST"
    echo "  Port: $MLFLOW_PORT"
    echo "  Backend Store: $MLFLOW_BACKEND_STORE_URI"
    echo "  Artifact Root: $MLFLOW_DEFAULT_ARTIFACT_ROOT"
    echo
}

# Main function
main() {
    case "${1:-start}" in
        "start")
            echo "=========================================="
            echo "MLflow Server Startup Script"
            echo "Diabetes Readmission Prediction Project"
            echo "=========================================="
            echo
            
            check_prerequisites
            create_directories
            init_database
            start_mlflow_server
            test_mlflow_connection
            log_pipeline_results
            
            echo
            echo "=========================================="
            print_success "MLflow server setup completed!"
            echo "=========================================="
            echo
            print_status "Access MLflow UI at: http://$MLFLOW_HOST:$MLFLOW_PORT"
            print_status "View logs at: ./mlflow_logs/mlflow_server.log"
            print_status "Stop server with: $0 stop"
            ;;
        "stop")
            stop_mlflow_server
            ;;
        "status")
            show_status
            ;;
        "restart")
            stop_mlflow_server
            sleep 2
            main start
            ;;
        "test")
            test_mlflow_connection
            ;;
        "log-results")
            log_pipeline_results
            ;;
        *)
            echo "Usage: $0 {start|stop|restart|status|test|log-results}"
            echo
            echo "Commands:"
            echo "  start       Start MLflow server (default)"
            echo "  stop        Stop MLflow server"
            echo "  restart     Restart MLflow server"
            echo "  status      Show MLflow server status"
            echo "  test        Test MLflow connection"
            echo "  log-results Log your pipeline results"
            echo
            echo "Environment Variables:"
            echo "  MLFLOW_HOST                    MLflow server host (default: 0.0.0.0)"
            echo "  MLFLOW_PORT                    MLflow server port (default: 5000)"
            echo "  MLFLOW_BACKEND_STORE_URI       Backend store URI (default: sqlite:///mlflow.db)"
            echo "  MLFLOW_DEFAULT_ARTIFACT_ROOT   Artifact root directory (default: ./mlflow_artifacts)"
            echo "  MLFLOW_CONFIG_FILE             Config file path (default: ./mlflow.conf)"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
