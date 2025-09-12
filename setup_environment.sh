#!/bin/bash

# Diabetes Readmission Prediction - Environment Setup Script
# This script sets up the Python environment for running the notebook

echo "🐍 Setting up Python environment for Diabetes Readmission Prediction..."

# Check if conda is available
if command -v conda &> /dev/null; then
    echo "✅ Conda found! Using conda environment..."
    
    # Create conda environment
    echo "📦 Creating conda environment..."
    conda env create -f environment.yml
    
    # Activate environment
    echo "🔄 Activating environment..."
    conda activate diabetes-readmission
    
    echo "✅ Conda environment setup complete!"
    echo "To activate: conda activate diabetes-readmission"
    
elif command -v python3 &> /dev/null; then
    echo "✅ Python3 found! Using virtual environment..."
    
    # Create virtual environment
    echo "📦 Creating virtual environment..."
    python3 -m venv diabetes-readmission-env
    
    # Activate environment
    echo "🔄 Activating environment..."
    source diabetes-readmission-env/bin/activate
    
    # Upgrade pip
    echo "⬆️ Upgrading pip..."
    pip install --upgrade pip
    
    # Install requirements
    echo "📥 Installing requirements..."
    pip install -r requirements-notebook.txt
    
    echo "✅ Virtual environment setup complete!"
    echo "To activate: source diabetes-readmission-env/bin/activate"
    
else
    echo "❌ Neither conda nor python3 found!"
    echo "Please install Python 3.9+ or Anaconda/Miniconda"
    exit 1
fi

echo ""
echo "🎉 Environment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Activate the environment (see command above)"
echo "2. Start Jupyter: jupyter notebook"
echo "3. Open: notebooks/01_Diabetic_Readmission_Complete_Pipeline.ipynb"
echo "4. Follow the leakage fix guide step by step"
echo ""
echo "🔧 For leakage fixes, follow the step-by-step guide provided!"



