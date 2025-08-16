#!/usr/bin/env python3
"""
Run Continuous Cagematch Scraper
=================================

Simple script to run the continuous scraper with different options.
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("Continuous Cagematch Scraper Runner")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python run_continuous_scraper.py expand [count]  - Expand database to specified count")
        print("  python run_continuous_scraper.py update          - Start continuous daily updates")
        print("  python run_continuous_scraper.py summary        - Show database summary")
        print("  python run_continuous_scraper.py validate       - Validate all data quality")
        print("  python run_continuous_scraper.py install        - Install required dependencies")
        print("  python run_continuous_scraper.py start          - Start both scraper and API")
        return
    
    command = sys.argv[1]
    
    if command == "install":
        print("Installing required dependencies...")
        success, stdout, stderr = run_command("pip install -r requirements_continuous.txt")
        if success:
            print("Dependencies installed successfully!")
        else:
            print(f"Error installing dependencies: {stderr}")
    
    elif command == "expand":
        count = sys.argv[2] if len(sys.argv) > 2 else "100"
        print(f"Expanding database to {count} wrestlers...")
        success, stdout, stderr = run_command(f"python continuous_cagematch_scraper.py expand {count}")
        if success:
            print("Database expansion completed!")
            print(stdout)
        else:
            print(f"Error expanding database: {stderr}")
    
    elif command == "update":
        print("Starting continuous update cycle...")
        print("Press Ctrl+C to stop")
        success, stdout, stderr = run_command("python continuous_cagematch_scraper.py update")
        if not success:
            print(f"Error in update cycle: {stderr}")
    
    elif command == "summary":
        print("Getting database summary...")
        success, stdout, stderr = run_command("python continuous_cagematch_scraper.py summary")
        if success:
            print(stdout)
        else:
            print(f"Error getting summary: {stderr}")
    
    elif command == "validate":
        print("Validating data quality...")
        success, stdout, stderr = run_command("python continuous_cagematch_scraper.py validate")
        if success:
            print(stdout)
        else:
            print(f"Error validating data: {stderr}")
    
    elif command == "start":
        print("Starting both continuous scraper and API...")
        
        # Start the API in background
        print("Starting API server...")
        api_process = subprocess.Popen([
            "python", "wrestling_api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for API to start
        import time
        time.sleep(3)
        
        # Start the continuous scraper
        print("Starting continuous scraper...")
        scraper_process = subprocess.Popen([
            "python", "continuous_cagematch_scraper.py", "update"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("Both services started!")
        print("API: http://localhost:5001")
        print("Scraper: Running in background")
        print("Press Ctrl+C to stop both services")
        
        try:
            # Wait for both processes
            api_process.wait()
            scraper_process.wait()
        except KeyboardInterrupt:
            print("\nStopping services...")
            api_process.terminate()
            scraper_process.terminate()
            print("Services stopped")
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'python run_continuous_scraper.py' to see available commands")

if __name__ == "__main__":
    main()
