import sys
from pathlib import Path

# Add notebooks directory to Python path
notebooks_path = Path(__file__).parent.parent / "notebooks"
sys.path.insert(0, str(notebooks_path))

# Import the FastAPI app
from app_improved import app  # noqa: E402

# Export the app for Vercel
handler = app
