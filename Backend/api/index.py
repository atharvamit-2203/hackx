#!/usr/bin/env python3
"""
Redirect to the correct API server with dependency installation
"""
import sys
import os
import subprocess

# Install dependencies first
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "fastapi", "uvicorn", "python-multipart", "python-dotenv", "pymongo", "firebase-admin", "pyyaml", "joblib", "numpy"])
    print("✅ Dependencies installed successfully")
except Exception as e:
    print(f"⚠️ Dependency installation failed: {e}")

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import and run the correct server
from api_server import app
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
