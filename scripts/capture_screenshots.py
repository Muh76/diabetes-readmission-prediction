#!/usr/bin/env python3
"""
Screenshot Capture Script for Diabetes Readmission Prediction

This script helps capture screenshots of the API interface and dashboards
for documentation purposes. It provides guidance on what to capture.

Usage:
    python scripts/capture_screenshots.py

The script will:
1. Check if the API is running
2. Provide guidance on what screenshots to capture
3. Suggest optimal screenshot settings
4. List all the screenshots needed
"""

import time
import webbrowser
from pathlib import Path

import requests


def check_api_status():
    """Check if the API is running locally."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running at http://localhost:8000")
            return True
        else:
            print("⚠️  API responded but with unexpected status")
            return False
    except requests.exceptions.RequestException:
        print("❌ API is not running. Please start it first:")
        print("   cd notebooks && python app.py")
        return False


def print_screenshot_guide():
    """Print comprehensive screenshot capture guide."""
    print("\n" + "=" * 60)
    print("📸 SCREENSHOT CAPTURE GUIDE")
    print("=" * 60)

    print("\n🎯 **RECOMMENDED SCREENSHOT SETTINGS:**")
    print("   • Resolution: 1920x1080 or higher")
    print("   • Format: PNG or JPG")
    print("   • Browser: Chrome or Firefox")
    print("   • Full-screen captures for dashboards")

    print("\n📱 **SCREENSHOTS TO CAPTURE:**")

    print("\n1️⃣ **API Interface Screenshots:**")
    print("   • Swagger UI (/docs): http://localhost:8000/docs")
    print("   • Health Check Response: http://localhost:8000/health")
    print("   • API Root: http://localhost:8000/")

    print("\n2️⃣ **Dashboard Screenshots:**")
    print("   • Executive Summary: notebooks/executive_summary_final.html")
    print("   • ROI Validation: notebooks/roi_validation_dashboard.html")
    print("   • Risk Mitigation: notebooks/risk_mitigation_dashboard.html")
    print("   • Business Metrics: notebooks/business_metrics_final.html")
    print("   • Clinical Outcomes: notebooks/clinical_outcomes_final.html")
    print(
        "   • Technical Documentation: notebooks/technical_documentation_dashboard.html"
    )

    print("\n3️⃣ **Model Performance Screenshots:**")
    print("   • Performance metrics from notebooks")
    print("   • Feature importance plots")
    print("   • Confusion matrices")
    print("   • ROC-AUC curves")

    print("\n4️⃣ **System Architecture Screenshots:**")
    print("   • MLflow tracking interface")
    print("   • Docker container status")
    print("   • Project file structure")

    print("\n💡 **CAPTURE TIPS:**")
    print("   • Use consistent browser window sizes")
    print("   • Include relevant data in screenshots")
    print("   • Capture both light and dark themes if available")
    print("   • Show interactive elements (hover states, etc.)")
    print("   • Include sample data that looks realistic")

    print("\n📁 **SAVE SCREENSHOTS TO:**")
    print("   • docs/screenshots/ (create this directory)")
    print("   • Use descriptive filenames:")
    print("     - api-swagger-ui.png")
    print("     - dashboard-executive-summary.png")
    print("     - model-performance-metrics.png")


def open_urls_for_screenshots():
    """Open URLs in browser for easy screenshot capture."""
    urls = [
        "http://localhost:8000/docs",
        "http://localhost:8000/health",
        "http://localhost:8000/",
    ]

    print("\n🌐 **Opening API URLs for screenshots:**")
    for url in urls:
        print(f"   Opening: {url}")
        try:
            webbrowser.open(url)
            time.sleep(1)  # Delay between opens
        except Exception as e:
            print(f"   Error opening {url}: {e}")


def create_screenshots_directory():
    """Create screenshots directory if it doesn't exist."""
    screenshots_dir = Path("docs/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 Created screenshots directory: {screenshots_dir}")

    # Create README for screenshots
    readme_content = """# Screenshots Directory

This directory contains screenshots of the Diabetes Readmission Prediction system.

## Screenshot Categories

### API Interface
- `api-swagger-ui.png` - Swagger documentation interface
- `api-health-check.png` - Health check response
- `api-root.png` - API root endpoint

### Dashboards
- `dashboard-executive-summary.png` - Executive summary dashboard
- `dashboard-roi-validation.png` - ROI validation dashboard
- `dashboard-risk-mitigation.png` - Risk mitigation dashboard
- `dashboard-business-metrics.png` - Business metrics dashboard
- `dashboard-clinical-outcomes.png` - Clinical outcomes dashboard
- `dashboard-technical-docs.png` - Technical documentation dashboard

### Model Performance
- `model-performance-metrics.png` - Performance metrics
- `model-feature-importance.png` - Feature importance plots
- `model-confusion-matrix.png` - Confusion matrix
- `model-roc-curve.png` - ROC-AUC curve

### System Architecture
- `mlflow-tracking.png` - MLflow experiment tracking
- `docker-status.png` - Docker container status
- `project-structure.png` - Project file structure

## Screenshot Guidelines

1. **Resolution**: Use 1920x1080 or higher
2. **Format**: PNG for best quality, JPG for smaller size
3. **Browser**: Chrome or Firefox recommended
4. **Content**: Include relevant data and interactive elements
5. **Naming**: Use descriptive, consistent filenames
"""

    readme_path = screenshots_dir / "README.md"
    with open(readme_path, "w") as f:
        f.write(readme_content)

    print(f"📝 Created screenshots README: {readme_path}")


def main():
    """Main function to run the screenshot capture guide."""
    print("📸 Diabetes Readmission Prediction - Screenshot Capture Guide")
    print("=" * 60)

    # Check API status
    api_running = check_api_status()

    # Create screenshots directory
    create_screenshots_directory()

    # Print comprehensive guide
    print_screenshot_guide()

    # Open URLs if API is running
    if api_running:
        open_urls_for_screenshots()
        print("\n🎉 **Ready to capture screenshots!**")
        print("   • Use the URLs above to navigate to different parts of the system")
        print("   • Take screenshots of each component")
        print("   • Save them to docs/screenshots/ with descriptive names")
    else:
        print("\n⚠️  **Start the API first to capture live screenshots:**")
        print("   cd notebooks && python app.py")
        print("   Then run this script again")

    print("\n📚 **Next Steps:**")
    print("   1. Capture all recommended screenshots")
    print("   2. Update README.md with screenshot references")
    print("   3. Add screenshots to GitHub repository")
    print("   4. Update documentation with visual examples")


if __name__ == "__main__":
    main()
