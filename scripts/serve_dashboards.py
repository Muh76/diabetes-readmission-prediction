#!/usr/bin/env python3
"""
Dashboard Server for Diabetes Readmission Prediction

This script serves the HTML dashboard files locally so they can be viewed
properly in a web browser.

Usage:
    python scripts/serve_dashboards.py

The server will:
1. Start a local HTTP server on port 8080
2. Serve all HTML dashboard files
3. Provide a navigation page to access all dashboards
4. Allow proper viewing of interactive Plotly dashboards
"""

import http.server
import os
import socketserver
import webbrowser
from pathlib import Path

# Configuration
PORT = 8080
DASHBOARDS_DIR = Path("notebooks")
BASE_URL = f"http://localhost:{PORT}"

# Dashboard files to serve
DASHBOARDS = {
    "executive_summary": "executive_summary_final.html",
    "roi_validation": "roi_validation_dashboard.html",
    "risk_mitigation": "risk_mitigation_dashboard.html",
    "business_metrics": "business_metrics_final.html",
    "clinical_outcomes": "clinical_outcomes_final.html",
    "technical_docs": "technical_documentation_dashboard.html",
    "cost_benefit": "cost_benefit_final.html",
    "final_roi_validation": "final_roi_validation_dashboard.html",
    "improved_risk_mitigation": "improved_risk_mitigation_dashboard.html",
    "technical_documentation": "technical_documentation_dashboard.html",
}


def create_index_html():
    """Create an index page that lists all available dashboards."""
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diabetes Readmission Prediction - Dashboard Hub</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .content {{
            padding: 40px;
        }}
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .dashboard-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #3498db;
            transition: all 0.3s ease;
            text-decoration: none;
            color: #333;
        }}
        .dashboard-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            border-left-color: #2c3e50;
        }}
        .dashboard-card h3 {{
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 1.3em;
        }}
        .dashboard-card p {{
            margin: 0;
            color: #666;
            line-height: 1.5;
        }}
        .status {{
            background: #e8f5e8;
            border: 1px solid #4caf50;
            color: #2e7d32;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .status::before {{
            content: "✅";
            font-size: 1.2em;
        }}
        .instructions {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .instructions h4 {{
            margin: 0 0 10px 0;
            font-size: 1.1em;
        }}
        .instructions ul {{
            margin: 5px 0;
            padding-left: 20px;
        }}
        .instructions li {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 Diabetes Readmission Prediction</h1>
            <p>Interactive Dashboard Hub</p>
        </div>

        <div class="content">
            <div class="status">
                Dashboard Server Running Successfully on Port {PORT}
            </div>

            <div class="instructions">
                <h4>📋 How to Use:</h4>
                <ul>
                    <li>Click on any dashboard below to view it in full screen</li>
                    <li>All dashboards are interactive with Plotly visualizations</li>
                    <li>Use browser back button to return to this hub</li>
                    <li>For best experience, use Chrome or Firefox</li>
                </ul>
            </div>

            <h2>📊 Available Dashboards</h2>
            <div class="dashboard-grid">
"""

    # Add dashboard cards
    for name, file in DASHBOARDS.items():
        if os.path.exists(DASHBOARDS_DIR / file):
            display_name = name.replace("_", " ").title()
            description = get_dashboard_description(name)

            html_content += f"""
                <a href="{file}" class="dashboard-card">
                    <h3>📈 {display_name}</h3>
                    <p>{description}</p>
                </a>"""

    html_content += """
            </div>
        </div>
    </div>
</body>
</html>
"""

    return html_content


def get_dashboard_description(name):
    """Get description for each dashboard."""
    descriptions = {
        "executive_summary": "High-level overview and key insights",
        "roi_validation": "Financial impact analysis and ROI projections",
        "risk_mitigation": "Risk management strategies and outcomes",
        "business_metrics": "KPI tracking and business performance",
        "clinical_outcomes": "Medical insights and patient outcomes",
        "technical_docs": "System architecture and technical details",
        "cost_benefit": "Cost-benefit analysis and projections",
        "final_roi_validation": "Comprehensive ROI validation results",
        "improved_risk_mitigation": "Enhanced risk mitigation strategies",
        "technical_documentation": "Complete technical documentation",
    }
    return descriptions.get(name, "Interactive dashboard with insights")


def start_server():
    """Start the HTTP server."""
    # Change to the dashboards directory
    os.chdir(DASHBOARDS_DIR)

    # Create index page
    index_html = create_index_html()
    with open("index.html", "w") as f:
        f.write(index_html)

    # Set up the server
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("🚀 Dashboard Server Started!")
        print(f"📍 URL: {BASE_URL}")
        print(f"📁 Serving from: {os.getcwd()}")
        print("📊 Dashboards available:")

        for name, file in DASHBOARDS.items():
            if os.path.exists(file):
                display_name = name.replace("_", " ").title()
                print(f"   ✅ {display_name}: {BASE_URL}/{file}")

        print(f"\n📋 Navigation Hub: {BASE_URL}/index.html")
        print("🎯 Opening in browser...")

        # Open in browser
        webbrowser.open(f"{BASE_URL}/index.html")

        print(f"\n🔧 Server running on port {PORT}")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            # Clean up index file
            if os.path.exists("index.html"):
                os.remove("index.html")
            print("✅ Cleanup complete")


if __name__ == "__main__":
    print("🏥 Diabetes Readmission Prediction - Dashboard Server")
    print("=" * 60)
    start_server()
