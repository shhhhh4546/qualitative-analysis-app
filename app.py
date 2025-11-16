"""Vercel entrypoint that exposes the FastAPI `app` from backend/main.py."""
from pathlib import Path
import sys

backend_dir = Path(__file__).resolve().parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from main import app  # type: ignore  # noqa: E402

