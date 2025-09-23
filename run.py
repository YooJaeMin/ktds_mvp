#!/usr/bin/env python3
"""
KTDS MVP - AI Services for Financial Business Strategy

This is a proof-of-concept application demonstrating AI-powered services
for IT companies targeting financial business acquisition.

Usage:
    python main.py

Requirements:
    - Python 3.8+
    - FastAPI
    - Azure AI Services (optional, will work with mock data if not configured)
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

if __name__ == "__main__":
    import uvicorn
    from main import app
    
    # Load environment variables from .env file if it exists
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
            print("✅ Environment variables loaded from .env file")
        except ImportError:
            print("⚠️  python-dotenv not installed. Continuing without .env file loading.")
    
    print("🚀 Starting KTDS MVP - AI Services for Financial Business Strategy")
    print("📖 Access the application at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "localhost"),
        port=int(os.getenv("PORT", 8000)),
        reload=False,  # Disable reload for now
        log_level="info"
    )