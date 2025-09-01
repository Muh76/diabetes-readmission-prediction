#!/usr/bin/env python3
"""
Direct FastAPI Entry Point for Railway
This file directly starts the improved FastAPI application without directory changes
"""

import os
import sys

import uvicorn

# Add notebooks directory to Python path
notebooks_path = os.path.join(os.getcwd(), "notebooks")
if notebooks_path not in sys.path:
    sys.path.insert(0, notebooks_path)


def main():
    """Start the improved FastAPI application directly"""
    print("🚀 Starting Improved Diabetes Readmission API...")

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

    # Import the FastAPI app
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "app_improved", os.path.join(notebooks_path, "app_improved.py")
        )
        app_improved = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_improved)
        print("✅ Successfully imported FastAPI app")
    except ImportError as e:
        print(f"❌ Failed to import app: {e}")
        return 1

    # Start the FastAPI application
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting server on port {port}...")

    uvicorn.run("app_improved:app", host="0.0.0.0", port=port, log_level="info")


if __name__ == "__main__":
    sys.exit(main())
