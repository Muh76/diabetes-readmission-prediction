#!/usr/bin/env python3
"""
Script to verify that all required dashboard screenshot files exist.
"""

from pathlib import Path

# Required screenshot files
REQUIRED_SCREENSHOTS = [
    "executive_summary.png",
    "clinical_outcomes.png",
    "clinical_insights.png",
    "roi_validation.png",
    "risk_mitigation.png",
    "business_metrics.png",
    "cost_benefit.png",
    "business_cases.png",
    "technical_documentation.png",
    "technical_implementation.png",
    "model_performance.png",
    "shap_analysis.png",
    "data_distribution.png",
    "hypothesis_testing.png",
    "lime_analysis.png",
]


def verify_screenshots():
    """Verify that all required screenshot files exist."""

    assets_dir = Path("assets/dashboards")

    print("🔍 Checking for required dashboard screenshots...")
    print(f"📁 Looking in: {assets_dir.absolute()}")
    print()

    missing_files = []
    existing_files = []

    for screenshot in REQUIRED_SCREENSHOTS:
        file_path = assets_dir / screenshot

        if file_path.exists():
            file_size = file_path.stat().st_size
            size_mb = file_size / (1024 * 1024)
            existing_files.append((screenshot, size_mb))
            print(f"✅ {screenshot} ({size_mb:.2f} MB)")
        else:
            missing_files.append(screenshot)
            print(f"❌ {screenshot} - MISSING")

    print()
    print("📊 Summary:")
    print(f"✅ Found: {len(existing_files)} screenshots")
    print(f"❌ Missing: {len(missing_files)} screenshots")

    if missing_files:
        print()
        print("🚨 Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        print()
        print("💡 To capture these screenshots:")
        print("   1. Run: python scripts/serve_dashboards.py")
        print("   2. Open: http://localhost:8080")
        print("   3. Capture screenshots and save to assets/dashboards/")
        print("   4. Use the exact filenames listed above")
    else:
        print()
        print("🎉 All screenshots are present!")
        print(f"📈 Total size: {sum(size for _, size in existing_files):.2f} MB")
        print()
        print("🚀 Ready to commit and push to GitHub!")
        print("   git add assets/dashboards/*.png")
        print("   git commit -m 'Add dashboard screenshots'")
        print("   git push origin master")


if __name__ == "__main__":
    verify_screenshots()
