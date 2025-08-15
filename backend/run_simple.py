#!/usr/bin/env python3
"""
Startup script for the simplified integrated wrestling platform
Focuses on wrestling statistics functionality
"""

import sys
import os

try:
    import uvicorn
    from integrated_app_simple import app
    
    print("🏆 Starting Ultimate Wrestling Platform (Simplified)...")
    print("📊 Features: Wrestling Statistics")
    print("🌐 API Documentation: http://localhost:8002/docs")
    print("📈 Stats Endpoints: /stats/*")
    print("🔍 Health Check: /health")
    
    # Start the integrated FastAPI application
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8002,
        reload=False,
        log_level="info"
    )
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Make sure you have installed all dependencies:")
    print("   pip install -r requirements_integrated_simple.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Startup Error: {e}")
    print("💡 Check the configuration and dependencies")
    sys.exit(1)
