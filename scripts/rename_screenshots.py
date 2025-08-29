#!/usr/bin/env python3
"""
Script to rename screenshot files to match the expected names in README.md
"""

from pathlib import Path

# Expected filenames that match the README
EXPECTED_NAMES = [
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


def rename_screenshots():
    """Rename screenshot files to expected names."""

    assets_dir = Path("assets/dashboards")

    # Get all PNG files
    png_files = list(assets_dir.glob("*.png"))
    png_files = [f for f in png_files if f.name != "README.md"]

    print(f"🔍 Found {len(png_files)} PNG files to rename")
    print()

    # Sort files by creation time to maintain order
    png_files.sort(key=lambda x: x.stat().st_ctime)

    # Rename files
    for i, (old_path, new_name) in enumerate(zip(png_files, EXPECTED_NAMES)):
        new_path = assets_dir / new_name

        if old_path.name != new_name:
            print(f"📝 Renaming {i+1:2d}/15: {old_path.name}")
            print(f"    → {new_name}")

            # If target file exists, remove it first
            if new_path.exists():
                new_path.unlink()
                print(f"    ⚠️  Removed existing {new_name}")

            # Rename the file
            old_path.rename(new_path)
            print("    ✅ Successfully renamed")
        else:
            print(f"✅ {i+1:2d}/15: {new_name} (already correct)")

        print()

    print("🎉 All screenshots have been renamed!")
    print()
    print("📋 Files are now named:")
    for name in EXPECTED_NAMES:
        print(f"   - {name}")
    print()
    print("🚀 Ready to commit and push to GitHub!")


if __name__ == "__main__":
    rename_screenshots()
