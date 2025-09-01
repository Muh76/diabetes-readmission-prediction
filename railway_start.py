#!/usr/bin/env python3
"""
Railway Entry Point for Improved Diabetes Readmission API
This file ensures Railway starts the correct FastAPI application
"""

import os
import subprocess
import sys


def main():
    """Start the improved FastAPI application"""
    print("🚀 Starting Improved Diabetes Readmission API...")

    # Change to notebooks directory
    notebooks_dir = os.path.join(os.getcwd(), "notebooks")
    if os.path.exists(notebooks_dir):
        os.chdir(notebooks_dir)
        print(f"📁 Changed to directory: {os.getcwd()}")

    # Check if the improved app exists
    app_file = "app_improved.py"
    if not os.path.exists(app_file):
        print(f"❌ Error: {app_file} not found in {os.getcwd()}")
        print("📁 Available files:")
        for file in os.listdir("."):
            if file.endswith(".py"):
                print(f"   - {file}")
        return 1

    # Start the FastAPI application
    print(f"✅ Starting {app_file}...")

    # Use uvicorn to start the FastAPI app
    port = int(os.environ.get("PORT", 8000))
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "app_improved:app",
        "--host",
        "0.0.0.0",
        "--port",
        str(port),
    ]

    print(f"🚀 Running: {' '.join(cmd)}")
    subprocess.run(cmd)


if __name__ == "__main__":
    sys.exit(main())
