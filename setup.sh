#!/bin/bash

echo "🚀 Setting up Diabetes Readmission Prediction Project Environment"
echo "================================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing project dependencies..."
pip install -e ".[dev]"

# Install pre-commit hooks
echo "🔒 Setting up pre-commit hooks..."
pre-commit install
pre-commit install --hook-type commit-msg

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your Azure credentials"
fi

# Create initial directories if they don't exist
echo "📁 Creating necessary directories..."
mkdir -p reports/{eda,models,monitoring}
mkdir -p data
mkdir -p logs

# Copy data file to data directory
if [ -f diabetic_data.csv ]; then
    echo "📊 Moving dataset to data directory..."
    mv diabetic_data.csv data/
fi

echo ""
echo "🎉 Environment setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Azure credentials"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Start MLflow: make mlflow-ui"
echo "4. Run EDA: jupyter notebook notebooks/01_initial_eda.ipynb"
echo "5. Check available commands: make help"
echo ""
echo "Happy coding! 🚀"
