#!/bin/bash

# Streamlit Cloud Deployment Script
# Diabetes Readmission Prediction Dashboard

set -e  # Exit on any error

# Configuration
REPO_NAME="diabetes-readmission-prediction"
STREAMLIT_APP_FILE="streamlit_app_comprehensive.py"
REQUIREMENTS_FILE="requirements-streamlit-cloud.txt"
GITHUB_USERNAME=${GITHUB_USERNAME:-"your-username"}

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
    
    if ! command_exists git; then
        print_error "Git is not installed. Please install it first."
        exit 1
    fi
    
    if ! command_exists python; then
        print_error "Python is not installed. Please install it first."
        exit 1
    fi
    
    if ! command_exists streamlit; then
        print_warning "Streamlit is not installed. Installing..."
        pip install streamlit
    fi
    
    print_success "All prerequisites are met!"
}

# Validate files
validate_files() {
    print_status "Validating required files..."
    
    if [ ! -f "$STREAMLIT_APP_FILE" ]; then
        print_error "Streamlit app file not found: $STREAMLIT_APP_FILE"
        exit 1
    fi
    
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        print_error "Requirements file not found: $REQUIREMENTS_FILE"
        exit 1
    fi
    
    # Check if models directory exists
    if [ ! -d "models" ]; then
        print_warning "Models directory not found. Creating demo structure..."
        mkdir -p models
        # Create dummy model files for demo
        python -c "
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Create dummy model for demo
dummy_model = RandomForestClassifier(n_estimators=10, random_state=42)
dummy_model.fit(np.random.rand(100, 5), np.random.randint(0, 2, 100))

# Save dummy files
joblib.dump(dummy_model, 'models/lightgbm_optimized.pkl')
joblib.dump(np.random.rand(5), 'models/feature_scaler.pkl')
joblib.dump(['feature1', 'feature2', 'feature3', 'feature4', 'feature5'], 'models/feature_names.pkl')
print('Demo model files created')
"
    fi
    
    print_success "All required files are present!"
}

# Test Streamlit app locally
test_app_locally() {
    print_status "Testing Streamlit app locally..."
    
    # Test if the app can be imported
    python -c "
import sys
sys.path.append('.')
try:
    import streamlit as st
    print('✅ Streamlit imported successfully')
    
    # Test if the app file can be imported
    import importlib.util
    spec = importlib.util.spec_from_file_location('streamlit_app', '$STREAMLIT_APP_FILE')
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    print('✅ Streamlit app imports successfully')
    
except Exception as e:
    print(f'❌ Error testing app: {str(e)}')
    exit(1)
"
    
    if [ $? -eq 0 ]; then
        print_success "Streamlit app test passed!"
    else
        print_error "Streamlit app test failed!"
        exit 1
    fi
}

# Check Git repository
check_git_repo() {
    print_status "Checking Git repository..."
    
    if [ ! -d ".git" ]; then
        print_error "Not a Git repository. Please initialize Git first:"
        echo "git init"
        echo "git add ."
        echo "git commit -m 'Initial commit'"
        exit 1
    fi
    
    # Check if there are uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        print_warning "There are uncommitted changes. Please commit them first:"
        echo "git add ."
        echo "git commit -m 'Update for Streamlit Cloud deployment'"
        exit 1
    fi
    
    print_success "Git repository is ready!"
}

# Push to GitHub
push_to_github() {
    print_status "Pushing to GitHub..."
    
    # Check if remote origin exists
    if ! git remote get-url origin >/dev/null 2>&1; then
        print_error "No remote origin found. Please add GitHub remote:"
        echo "git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
        exit 1
    fi
    
    # Push to GitHub
    git push origin main
    
    if [ $? -eq 0 ]; then
        print_success "Code pushed to GitHub successfully!"
    else
        print_error "Failed to push to GitHub!"
        exit 1
    fi
}

# Create deployment instructions
create_deployment_instructions() {
    print_status "Creating deployment instructions..."
    
    cat > DEPLOYMENT_INSTRUCTIONS.md << EOF
# 🚀 Streamlit Cloud Deployment Instructions

## Quick Deployment Steps

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with your GitHub account**
3. **Click "New app"**
4. **Fill in the deployment form:**
   - **Repository:** \`$GITHUB_USERNAME/$REPO_NAME\`
   - **Branch:** \`main\`
   - **Main file path:** \`$STREAMLIT_APP_FILE\`
   - **App URL:** \`$REPO_NAME\` (or your preferred name)

5. **Click "Deploy!"**

## Your App Configuration

- **App File:** \`$STREAMLIT_APP_FILE\`
- **Requirements:** \`$REQUIREMENTS_FILE\`
- **Repository:** \`https://github.com/$GITHUB_USERNAME/$REPO_NAME\`

## Expected App URL

Once deployed, your app will be available at:
\`https://$REPO_NAME-$GITHUB_USERNAME.streamlit.app\`

## Features Included

✅ Interactive patient prediction form  
✅ Real-time risk assessment  
✅ Business impact analysis  
✅ Model performance metrics  
✅ Data visualizations  
✅ Responsive design  
✅ Error handling  

## Support

If you encounter any issues:
1. Check the Streamlit Cloud logs
2. Verify all files are in the repository
3. Ensure requirements.txt is correct
4. Test locally with \`streamlit run $STREAMLIT_APP_FILE\`

EOF
    
    print_success "Deployment instructions created!"
}

# Main deployment function
main() {
    echo "=========================================="
    echo "Streamlit Cloud Deployment Script"
    echo "Diabetes Readmission Prediction Dashboard"
    echo "=========================================="
    echo
    
    check_prerequisites
    validate_files
    test_app_locally
    check_git_repo
    push_to_github
    create_deployment_instructions
    
    echo
    echo "=========================================="
    print_success "Deployment preparation completed!"
    echo "=========================================="
    echo
    print_status "Next steps:"
    echo "1. Go to https://share.streamlit.io"
    echo "2. Sign in with your GitHub account"
    echo "3. Click 'New app'"
    echo "4. Use repository: $GITHUB_USERNAME/$REPO_NAME"
    echo "5. Set main file: $STREAMLIT_APP_FILE"
    echo "6. Click 'Deploy!'"
    echo
    print_status "Your app will be available at:"
    echo "https://$REPO_NAME-$GITHUB_USERNAME.streamlit.app"
    echo
    print_status "Deployment instructions saved to: DEPLOYMENT_INSTRUCTIONS.md"
}

# Run main function
main "$@"
