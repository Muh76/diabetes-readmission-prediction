#!/usr/bin/env python3
"""
Railway Startup Script - Copy app to root and start
"""

import os
import shutil
import subprocess
import sys


def main():
    """Copy app to root and start FastAPI"""
    print("🚀 Starting Improved Diabetes Readmission API...")

    # Copy the improved app to root directory
    source_app = "notebooks/app_improved.py"
    target_app = "app.py"

    if os.path.exists(source_app):
        shutil.copy2(source_app, target_app)
        print(f"✅ Copied {source_app} to {target_app}")
    else:
        print(f"❌ Error: {source_app} not found")
        return 1

    # Start the FastAPI application
    port = os.environ.get("PORT", "8000")
    print(f"🚀 Starting server on port {port}...")

    # Use uvicorn to start the app
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "app:app",
        "--host",
        "0.0.0.0",
        "--port",
        port,
    ]

    print(f"🚀 Running: {' '.join(cmd)}")
    subprocess.run(cmd)


if __name__ == "__main__":
    sys.exit(main())
