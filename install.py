#!/usr/bin/env python3
"""
Installation script for the Bangladeshi Fitness App
This script installs all required dependencies and sets up the environment
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python {version.major}.{version.minor} is not supported.")
        print("Please install Python 3.7 or higher.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    dependencies = [
        "kivy==2.2.1",
        "kivymd==1.1.1",
        "pillow==10.0.0",
        "requests==2.31.0",
        "python-dotenv==1.0.0",
        "mysql-connector-python==8.2.0",
        "pymysql==1.1.0"
    ]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
            return False
    
    return True

def check_system_requirements():
    """Check system requirements for Kivy"""
    print("\n🖥️ Checking system requirements...")
    
    system = platform.system()
    print(f"Operating System: {system}")
    
    if system == "Darwin":  # macOS
        print("✅ macOS detected - Kivy should work well")
    elif system == "Linux":
        print("✅ Linux detected - Kivy should work well")
    elif system == "Windows":
        print("⚠️ Windows detected - Kivy may require additional setup")
    else:
        print(f"⚠️ Unknown system: {system}")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "data",
        "logs",
        "exports"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory already exists: {directory}")
    
    return True

def run_tests():
    """Run the test suite"""
    print("\n🧪 Running tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_app.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def setup_mysql():
    """Setup MySQL database"""
    print("\n🗄️ Setting up MySQL database...")
    
    try:
        result = subprocess.run([sys.executable, "setup_mysql.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ MySQL setup completed!")
            return True
        else:
            print("⚠️ MySQL setup had issues:")
            print(result.stdout)
            print(result.stderr)
            print("You can run setup_mysql.py manually later")
            return True  # Don't fail installation
            
    except Exception as e:
        print(f"❌ Failed to setup MySQL: {e}")
        print("You can run setup_mysql.py manually later")
        return True  # Don't fail installation

def create_launcher_script():
    """Create a launcher script for easy app startup"""
    print("\n🚀 Creating launcher script...")
    
    launcher_content = """#!/usr/bin/env python3
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the app
from main import BangladeshiFitnessApp

if __name__ == '__main__':
    BangladeshiFitnessApp().run()
"""
    
    with open("run_app.py", "w") as f:
        f.write(launcher_content)
    
    # Make it executable on Unix systems
    if platform.system() != "Windows":
        os.chmod("run_app.py", 0o755)
    
    print("✅ Launcher script created: run_app.py")
    return True

def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "="*60)
    print("🎉 Installation Complete!")
    print("="*60)
    print("\nTo run the Bangladeshi Fitness App:")
    print("1. python3 run_app.py")
    print("   or")
    print("2. python3 main.py")
    print("\nTo run tests:")
    print("   python3 test_app.py")
    print("\nApp Features:")
    print("✅ Complete Bangla language support")
    print("✅ Local Bangladeshi food database")
    print("✅ Exercise tracking with difficulty levels")
    print("✅ Digital pantry for quick food access")
    print("✅ Calorie and macro tracking")
    print("✅ User-friendly interface")
    print("\nFor support or questions, check the README.md file")
    print("="*60)

def main():
    """Main installation function"""
    print("🚀 Bangladeshi Fitness App Installation")
    print("="*50)
    
    steps = [
        ("Python Version Check", check_python_version),
        ("System Requirements", check_system_requirements),
        ("Dependencies Installation", install_dependencies),
        ("Directory Creation", create_directories),
        ("MySQL Setup", setup_mysql),
        ("Test Suite", run_tests),
        ("Launcher Script", create_launcher_script)
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ {step_name} failed. Installation aborted.")
            return False
    
    print_usage_instructions()
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 