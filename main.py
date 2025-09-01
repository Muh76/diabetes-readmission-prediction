#!/usr/bin/env python3
"""
Simple FastAPI Entry Point for Railway
This file directly starts the improved FastAPI application
"""

import os
import sys

import uvicorn


def main():
    """Start the improved FastAPI application"""
    print("🚀 Starting Improved Diabetes Readmission API...")

    # Add notebooks directory to Python path
    notebooks_path = os.path.join(os.getcwd(), "notebooks")
    if notebooks_path not in sys.path:
        sys.path.insert(0, notebooks_path)

    # Check if the improved app exists
    app_file = os.path.join(notebooks_path, "app_improved.py")
    if not os.path.exists(app_file):
        print(f"❌ Error: {app_file} not found")
        print("📁 Available files in notebooks:")
        if os.path.exists(notebooks_path):
            for file in os.listdir(notebooks_path):
                if file.endswith(".py"):
                    print(f"   - {file}")
        return 1

    print(f"✅ Found {app_file}")

    # Start the FastAPI application directly
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting server on port {port}...")

    # Use uvicorn to start the app directly from the file
    uvicorn.run(
        "notebooks.app_improved:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=False,
    )


if __name__ == "__main__":
    sys.exit(main())
