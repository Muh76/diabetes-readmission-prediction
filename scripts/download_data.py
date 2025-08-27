#!/usr/bin/env python3
"""
Data Download Script for Diabetes Readmission Prediction

This script downloads the UCI Diabetes Dataset from the official repository
and prepares it for use in the diabetes readmission prediction project.

Usage:
    python scripts/download_data.py

The script will:
1. Download the dataset from UCI ML Repository
2. Create a sample dataset (1,000 rows) for testing
3. Save both full and sample datasets
4. Update .gitignore to exclude large files
"""

import os
import pandas as pd
import requests
import zipfile
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
UCI_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00296/dataset_diabetes.zip"
DATA_DIR = Path("data")
SAMPLE_SIZE = 1000

def create_directories():
    """Create necessary directories if they don't exist."""
    DATA_DIR.mkdir(exist_ok=True)
    Path("scripts").mkdir(exist_ok=True)
    logger.info(f"Created directories: {DATA_DIR}")

def download_dataset():
    """Download the dataset from UCI ML Repository."""
    zip_path = DATA_DIR / "dataset_diabetes.zip"
    
    if zip_path.exists():
        logger.info("Dataset already exists, skipping download")
        return zip_path
    
    logger.info(f"Downloading dataset from {UCI_URL}")
    response = requests.get(UCI_URL, stream=True)
    response.raise_for_status()
    
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    logger.info(f"Downloaded {zip_path}")
    return zip_path

def extract_dataset(zip_path):
    """Extract the ZIP file and return the CSV path."""
    extract_dir = DATA_DIR / "extracted"
    extract_dir.mkdir(exist_ok=True)
    
    logger.info(f"Extracting {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    # Find the CSV file
    csv_files = list(extract_dir.rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV file found in extracted archive")
    
    csv_path = csv_files[0]
    logger.info(f"Extracted dataset: {csv_path}")
    return csv_path

def process_dataset(csv_path):
    """Process the dataset and create sample versions."""
    logger.info(f"Processing dataset: {csv_path}")
    
    # Load the dataset
    df = pd.read_csv(csv_path)
    logger.info(f"Loaded dataset with shape: {df.shape}")
    
    # Create sample dataset
    sample_df = df.sample(n=min(SAMPLE_SIZE, len(df)), random_state=42)
    
    # Save full dataset
    full_path = DATA_DIR / "diabetic_data.csv"
    df.to_csv(full_path, index=False)
    logger.info(f"Saved full dataset: {full_path}")
    
    # Save sample dataset
    sample_path = DATA_DIR / "diabetic_data_sample.csv"
    sample_df.to_csv(sample_path, index=False)
    logger.info(f"Saved sample dataset: {sample_path}")
    
    # Create data info file
    info_path = DATA_DIR / "dataset_info.txt"
    with open(info_path, 'w') as f:
        f.write(f"Dataset Information\n")
        f.write(f"==================\n")
        f.write(f"Source: UCI Machine Learning Repository\n")
        f.write(f"Full Dataset: {len(df)} rows, {len(df.columns)} columns\n")
        f.write(f"Sample Dataset: {len(sample_df)} rows, {len(sample_df.columns)} columns\n")
        f.write(f"Target Variable: readmitted\n")
        f.write(f"Date Downloaded: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    return full_path, sample_path

def update_gitignore():
    """Update .gitignore to exclude large data files."""
    gitignore_path = Path(".gitignore")
    
    # Read existing .gitignore
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            content = f.read()
    else:
        content = ""
    
    # Add data exclusions if not already present
    data_exclusions = [
        "\n# Data files (exclude large datasets)",
        "data/diabetic_data.csv",
        "data/dataset_diabetes.zip",
        "data/extracted/",
        "!data/diabetic_data_sample.csv",
        "!data/dataset_info.txt"
    ]
    
    for exclusion in data_exclusions:
        if exclusion not in content:
            content += exclusion + "\n"
    
    # Write updated .gitignore
    with open(gitignore_path, 'w') as f:
        f.write(content)
    
    logger.info("Updated .gitignore to exclude large data files")

def create_download_script():
    """Create a simple download script for users."""
    script_content = '''#!/bin/bash
# Quick data download script

echo "Downloading Diabetes Readmission Dataset..."
python scripts/download_data.py

echo "Data download complete!"
echo "- Full dataset: data/diabetic_data.csv"
echo "- Sample dataset: data/diabetic_data_sample.csv"
echo "- Dataset info: data/dataset_info.txt"
'''
    
    script_path = Path("download_data.sh")
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make executable
    os.chmod(script_path, 0o755)
    logger.info(f"Created download script: {script_path}")

def main():
    """Main function to orchestrate the download process."""
    try:
        logger.info("Starting dataset download process...")
        
        # Create directories
        create_directories()
        
        # Download dataset
        zip_path = download_dataset()
        
        # Extract dataset
        csv_path = extract_dataset(zip_path)
        
        # Process dataset
        full_path, sample_path = process_dataset(csv_path)
        
        # Update .gitignore
        update_gitignore()
        
        # Create download script
        create_download_script()
        
        logger.info("Dataset download and processing completed successfully!")
        logger.info(f"Full dataset: {full_path}")
        logger.info(f"Sample dataset: {sample_path}")
        logger.info("Use the sample dataset for development and testing.")
        
    except Exception as e:
        logger.error(f"Error during dataset download: {e}")
        raise

if __name__ == "__main__":
    main()
