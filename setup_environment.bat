@echo off
REM Diabetes Readmission Prediction - Environment Setup Script (Windows)
REM This script sets up the Python environment for running the notebook

echo 🐍 Setting up Python environment for Diabetes Readmission Prediction...

REM Check if conda is available
where conda >nul 2>nul
if %errorlevel% == 0 (
    echo ✅ Conda found! Using conda environment...
    
    REM Create conda environment
    echo 📦 Creating conda environment...
    conda env create -f environment.yml
    
    REM Activate environment
    echo 🔄 Activating environment...
    call conda activate diabetes-readmission
    
    echo ✅ Conda environment setup complete!
    echo To activate: conda activate diabetes-readmission
    goto :success
)

REM Check if python is available
where python >nul 2>nul
if %errorlevel% == 0 (
    echo ✅ Python found! Using virtual environment...
    
    REM Create virtual environment
    echo 📦 Creating virtual environment...
    python -m venv diabetes-readmission-env
    
    REM Activate environment
    echo 🔄 Activating environment...
    call diabetes-readmission-env\Scripts\activate.bat
    
    REM Upgrade pip
    echo ⬆️ Upgrading pip...
    python -m pip install --upgrade pip
    
    REM Install requirements
    echo 📥 Installing requirements...
    pip install -r requirements-notebook.txt
    
    echo ✅ Virtual environment setup complete!
    echo To activate: diabetes-readmission-env\Scripts\activate.bat
    goto :success
)

echo ❌ Neither conda nor python found!
echo Please install Python 3.9+ or Anaconda/Miniconda
exit /b 1

:success
echo.
echo 🎉 Environment setup complete!
echo.
echo 📋 Next steps:
echo 1. Activate the environment (see command above)
echo 2. Start Jupyter: jupyter notebook
echo 3. Open: notebooks/01_Diabetic_Readmission_Complete_Pipeline.ipynb
echo 4. Follow the leakage fix guide step by step
echo.
echo 🔧 For leakage fixes, follow the step-by-step guide provided!
pause



