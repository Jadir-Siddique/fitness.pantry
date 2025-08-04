#!/usr/bin/env python3
"""
Status checker for Bangladeshi Fitness App
Checks if the web server is running and provides information.
"""

import requests
import sys
import os

def check_server_status():
    """Check if the web server is running and return status."""
    try:
        response = requests.get('http://localhost:8080', timeout=5)
        if response.status_code == 200:
            return True, "✅ Server is running successfully!"
        else:
            return False, f"❌ Server responded with status code: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "❌ Server is not running. Start it with: python3 run_web_app.py"
    except requests.exceptions.Timeout:
        return False, "❌ Server connection timed out"
    except Exception as e:
        return False, f"❌ Error checking server: {e}"

def main():
    print("🏃‍♂️ Bangladeshi Fitness App - Status Check")
    print("=" * 50)
    
    # Check server status
    is_running, message = check_server_status()
    print(message)
    
    if is_running:
        print("\n📱 Access your app at:")
        print("   🌐 http://localhost:8080")
        print("   📱 Works on desktop, tablet, and mobile")
        
        print("\n🎯 Features available:")
        print("   ✅ Dashboard with daily summary")
        print("   ✅ Food tracking (Bangladeshi foods)")
        print("   ✅ Exercise tracking (multiple levels)")
        print("   ✅ Pantry management")
        print("   ✅ Profile settings")
        
        print("\n💡 Tips:")
        print("   • Add some foods and exercises to see data")
        print("   • Try the water tracking feature")
        print("   • Explore the Bengali interface")
        
    else:
        print("\n🔧 To start the server:")
        print("   1. python3 run_web_app.py")
        print("   2. Or: python3 web_app.py")
        print("   3. Then open: http://localhost:8080")
    
    print("\n" + "=" * 50)

if __name__ == '__main__':
    main() 