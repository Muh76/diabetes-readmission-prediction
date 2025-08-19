#!/bin/bash

# Azure Container Apps Deployment Script for ML API
# This script deploys the Diabetic Readmission ML API to Azure Container Apps

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Azure Configuration
RESOURCE_GROUP="Muh_Azure_ML"
LOCATION="eastus2"
ACR_NAME="diabetesmlacr"
CONTAINER_APP_ENV="diabetes-ml-env"
CONTAINER_APP_NAME="diabetes-ml-api"
IMAGE_NAME="diabetes-ml-api:latest"

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

# Function to check Azure CLI
check_azure_cli() {
    if ! command -v az &> /dev/null; then
        print_error "Azure CLI is not installed. Please install it first."
        exit 1
    fi

    # Check if logged in
    if ! az account show &> /dev/null; then
        print_error "Not logged in to Azure. Please run 'az login' first."
        exit 1
    fi

    print_success "Azure CLI is available and authenticated"
}

# Function to check resource group
check_resource_group() {
    if ! az group show --name $RESOURCE_GROUP &> /dev/null; then
        print_error "Resource group $RESOURCE_GROUP does not exist."
        exit 1
    fi
    print_success "Resource group $RESOURCE_GROUP exists"
}

# Function to check ACR
check_acr() {
    if ! az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
        print_error "ACR $ACR_NAME does not exist in resource group $RESOURCE_GROUP."
        exit 1
    fi
    print_success "ACR $ACR_NAME exists"
}

# Function to check Container Apps environment
check_container_app_env() {
    if ! az containerapp env show --name $CONTAINER_APP_ENV --resource-group $RESOURCE_GROUP &> /dev/null; then
        print_error "Container Apps environment $CONTAINER_APP_ENV does not exist."
        exit 1
    fi
    print_success "Container Apps environment $CONTAINER_APP_ENV exists"
}

# Function to create container app
create_container_app() {
    print_status "Creating Container App..."

    # Get ACR login server
    ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query loginServer --output tsv)

    # Create container app
    az containerapp create \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --environment $CONTAINER_APP_ENV \
        --image $ACR_LOGIN_SERVER/$IMAGE_NAME \
        --target-port 8000 \
        --ingress external \
        --allow-insecure \
        --cpu 1.0 \
        --memory 2.0Gi \
        --min-replicas 1 \
        --max-replicas 3 \
        --env-vars \
            PYTHONPATH=/app \
            PORT=8000 \
            LOG_LEVEL=INFO \
        --registry-server $ACR_LOGIN_SERVER \
        --registry-username $ACR_NAME \
        --registry-password $(az acr credential show --name $ACR_NAME --query "passwords[0].value" --output tsv) \
        --query properties.configuration.ingress.fqdn \
        --output tsv

    print_success "Container App created successfully"
}

# Function to update container app
update_container_app() {
    print_status "Updating Container App..."

    # Get ACR login server
    ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query loginServer --output tsv)

    # Update container app
    az containerapp update \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --image $ACR_LOGIN_SERVER/$IMAGE_NAME \
        --registry-server $ACR_LOGIN_SERVER \
        --registry-username $ACR_NAME \
        --registry-password $(az acr credential show --name $ACR_NAME --query "passwords[0].value" --output tsv)

    print_success "Container App updated successfully"
}

# Function to show container app info
show_container_app_info() {
    print_status "Container App Information:"
    echo

    # Get FQDN
    FQDN=$(az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn --output tsv)

    echo "🌐 API Endpoints:"
    echo "   • Main API: https://$FQDN"
    echo "   • Health Check: https://$FQDN/health"
    echo "   • API Documentation: https://$FQDN/docs"
    echo "   • Model Information: https://$FQDN/models"
    echo

    echo "📊 Container App Status:"
    az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query "{name:name, status:properties.provisioningState, revision:properties.latestRevisionName, replicas:properties.runningStatus.replicaCount}" --output table
    echo

    echo "📝 Container App Logs:"
    echo "   az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --follow"
    echo
}

# Function to test the API
test_api() {
    print_status "Testing API endpoints..."

    # Get FQDN
    FQDN=$(az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn --output tsv)

    # Wait for app to be ready
    print_status "Waiting for API to be ready..."
    sleep 30

    # Test health endpoint
    if curl -s "https://$FQDN/health" | grep -q "healthy"; then
        print_success "Health endpoint working"
    else
        print_error "Health endpoint failed"
    fi

    # Test models endpoint
    if curl -s "https://$FQDN/models" > /dev/null; then
        print_success "Models endpoint working"
    else
        print_error "Models endpoint failed"
    fi

    # Test prediction endpoint with sample data
    sample_data='{"num_medications": 5, "time_in_hospital": 7, "number_diagnoses": 3, "num_procedures": 1, "num_lab_procedures": 25}'
    if curl -s -X POST "https://$FQDN/predict" \
        -H "Content-Type: application/json" \
        -d "$sample_data" > /dev/null; then
        print_success "Prediction endpoint working"
    else
        print_error "Prediction endpoint failed"
    fi
}

# Function to delete container app
delete_container_app() {
    print_warning "This will delete the Container App. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Deleting Container App..."
        az containerapp delete --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --yes
        print_success "Container App deleted successfully"
    else
        print_status "Deletion cancelled"
    fi
}

# Function to show logs
show_logs() {
    print_status "Showing Container App logs..."
    az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --follow
}

# Function to scale container app
scale_container_app() {
    print_status "Scaling Container App..."
    echo "Current replicas: $(az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query properties.runningStatus.replicaCount --output tsv)"
    echo "Enter new number of replicas (1-10):"
    read -r replicas

    if [[ "$replicas" =~ ^[1-9]$|^10$ ]]; then
        az containerapp revision set-mode \
            --name $CONTAINER_APP_NAME \
            --resource-group $RESOURCE_GROUP \
            --mode single \
            --revision $(az containerapp revision list --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query "[0].name" --output tsv)

        az containerapp update \
            --name $CONTAINER_APP_NAME \
            --resource-group $RESOURCE_GROUP \
            --min-replicas $replicas \
            --max-replicas $replicas

        print_success "Container App scaled to $replicas replicas"
    else
        print_error "Invalid number of replicas"
    fi
}

# Main deployment function
deploy() {
    print_status "Starting Azure Container Apps deployment..."
    echo

    check_azure_cli
    check_resource_group
    check_acr
    check_container_app_env

    # Check if container app exists
    if az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
        print_warning "Container App $CONTAINER_APP_NAME already exists. Updating..."
        update_container_app
    else
        print_status "Creating new Container App..."
        create_container_app
    fi

    show_container_app_info
    test_api

    print_success "Deployment completed successfully!"
}

# Main script logic
case "${1:-deploy}" in
    "deploy")
        deploy
        ;;
    "update")
        update_container_app
        show_container_app_info
        ;;
    "info")
        show_container_app_info
        ;;
    "test")
        test_api
        ;;
    "logs")
        show_logs
        ;;
    "scale")
        scale_container_app
        ;;
    "delete")
        delete_container_app
        ;;
    *)
        echo "Usage: $0 {deploy|update|info|test|logs|scale|delete}"
        echo
        echo "Commands:"
        echo "  deploy   - Deploy/update the ML API (default)"
        echo "  update   - Update the existing Container App"
        echo "  info     - Show Container App information"
        echo "  test     - Test API endpoints"
        echo "  logs     - Show Container App logs"
        echo "  scale    - Scale the Container App"
        echo "  delete   - Delete the Container App"
        exit 1
        ;;
esac
