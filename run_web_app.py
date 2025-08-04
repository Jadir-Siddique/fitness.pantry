#!/usr/bin/env python3
"""
Bangladeshi Fitness App - Web Server Runner
This script runs the Flask web application for the fitness tracker.
"""

import sys
import os
import webbrowser
from time import sleep

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        # Import the web app
        from web_app import app
        
        print("🚀 Starting Bangladeshi Fitness App Web Server...")
        print("📱 Opening browser automatically in 3 seconds...")
        print("🌐 Server will be available at: http://localhost:8080")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Open browser after a short delay
        def open_browser():
            sleep(3)
            webbrowser.open('http://localhost:8080')
        
        # Start browser opening in background
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Run the app
        app.run(debug=True, host='0.0.0.0', port=8080)
        
    except ImportError as e:
        print(f"❌ Error importing web app: {e}")
        print("💡 Make sure you have installed all dependencies:")
        print("   pip3 install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error running server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 