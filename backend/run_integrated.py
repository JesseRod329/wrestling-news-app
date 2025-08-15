#!/usr/bin/env python3
"""
Startup script for the integrated wrestling platform
Combines wrestling statistics and news functionality
"""

import sys
import os
from pathlib import Path

# Add the parent directory to Python path to access newsite modules
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
newsite_dir = parent_dir / "newsite"

# Add newsite to Python path
if str(newsite_dir) not in sys.path:
    sys.path.insert(0, str(newsite_dir))

# Add newsite/app to Python path
newsite_app_dir = newsite_dir / "app"
if str(newsite_app_dir) not in sys.path:
    sys.path.insert(0, str(newsite_app_dir))

try:
    import uvicorn
    from integrated_app import app
    
    print("🏆 Starting Ultimate Wrestling Platform...")
    print("📊 Features: Wrestling Statistics + News Aggregation")
    print("🌐 API Documentation: http://localhost:8000/docs")
    print("📰 News Endpoints: /news/*")
    print("📈 Stats Endpoints: /stats/*")
    print("🔍 Health Check: /health")
    
    # Start the integrated FastAPI application
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Make sure you have installed all dependencies:")
    print("   pip install -r requirements_integrated.txt")
    print("💡 Make sure the newsite folder is accessible")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Startup Error: {e}")
    print("💡 Check the configuration and dependencies")
    sys.exit(1)
