#!/usr/bin/env python3
"""
MySQL Setup Script for Bangladeshi Fitness App
This script helps set up the MySQL database for the fitness app
"""

import mysql.connector
import os
import sys
from config import Config

def create_database():
    """Create the MySQL database if it doesn't exist"""
    print("🗄️ Creating MySQL database...")
    
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=Config.DATABASE_HOST,
            port=Config.DATABASE_PORT,
            user=Config.DATABASE_USER,
            password=Config.DATABASE_PASSWORD,
            charset=Config.DATABASE_CHARSET
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DATABASE_NAME}")
        print(f"✅ Database '{Config.DATABASE_NAME}' created/verified")
        
        # Use the database
        cursor.execute(f"USE {Config.DATABASE_NAME}")
        
        # Test connection
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ MySQL version: {version[0]}")
        
        connection.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ MySQL setup failed: {err}")
        return False

def test_connection():
    """Test the MySQL connection with the database"""
    print("\n🔍 Testing MySQL connection...")
    
    try:
        connection = mysql.connector.connect(
            host=Config.DATABASE_HOST,
            port=Config.DATABASE_PORT,
            user=Config.DATABASE_USER,
            password=Config.DATABASE_PASSWORD,
            database=Config.DATABASE_NAME,
            charset=Config.DATABASE_CHARSET
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result:
            print("✅ MySQL connection successful!")
            print(f"   - Host: {Config.DATABASE_HOST}")
            print(f"   - Port: {Config.DATABASE_PORT}")
            print(f"   - Database: {Config.DATABASE_NAME}")
            print(f"   - User: {Config.DATABASE_USER}")
        
        connection.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ MySQL connection failed: {err}")
        return False

def setup_environment_variables():
    """Create a .env file with database configuration"""
    print("\n📝 Setting up environment variables...")
    
    env_content = f"""# Database Configuration
DB_HOST={Config.DATABASE_HOST}
DB_PORT={Config.DATABASE_PORT}
DB_NAME={Config.DATABASE_NAME}
DB_USER={Config.DATABASE_USER}
DB_PASSWORD={Config.DATABASE_PASSWORD}

# App Configuration
FLASK_ENV=development
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def print_manual_setup_instructions():
    """Print manual setup instructions"""
    print("\n" + "="*60)
    print("📋 Manual MySQL Setup Instructions")
    print("="*60)
    print("\nIf automatic setup failed, follow these steps:")
    print("\n1. Install MySQL Server:")
    print("   - Ubuntu/Debian: sudo apt-get install mysql-server")
    print("   - macOS: brew install mysql")
    print("   - Windows: Download from mysql.com")
    
    print("\n2. Start MySQL Service:")
    print("   - Ubuntu/Debian: sudo systemctl start mysql")
    print("   - macOS: brew services start mysql")
    print("   - Windows: Start from Services")
    
    print("\n3. Create Database:")
    print("   mysql -u root -p")
    print(f"   CREATE DATABASE {Config.DATABASE_NAME};")
    print("   exit")
    
    print("\n4. Create User (Optional):")
    print("   mysql -u root -p")
    print(f"   CREATE USER '{Config.DATABASE_USER}'@'localhost' IDENTIFIED BY 'your_password';")
    print(f"   GRANT ALL PRIVILEGES ON {Config.DATABASE_NAME}.* TO '{Config.DATABASE_USER}'@'localhost';")
    print("   FLUSH PRIVILEGES;")
    print("   exit")
    
    print("\n5. Update Configuration:")
    print("   Edit config.py or set environment variables:")
    print(f"   - DB_HOST: {Config.DATABASE_HOST}")
    print(f"   - DB_PORT: {Config.DATABASE_PORT}")
    print(f"   - DB_NAME: {Config.DATABASE_NAME}")
    print(f"   - DB_USER: {Config.DATABASE_USER}")
    print(f"   - DB_PASSWORD: your_password")
    
    print("\n6. Test Connection:")
    print("   python3 setup_mysql.py")
    print("="*60)

def main():
    """Main setup function"""
    print("🚀 MySQL Setup for Bangladeshi Fitness App")
    print("="*50)
    
    # Check if MySQL connector is installed
    try:
        import mysql.connector
        print("✅ MySQL Connector/Python is installed")
    except ImportError:
        print("❌ MySQL Connector/Python not found")
        print("Install it with: pip install mysql-connector-python")
        return False
    
    # Create database
    if not create_database():
        print_manual_setup_instructions()
        return False
    
    # Test connection
    if not test_connection():
        print_manual_setup_instructions()
        return False
    
    # Setup environment variables
    setup_environment_variables()
    
    print("\n🎉 MySQL setup completed successfully!")
    print("\nYou can now run the app:")
    print("python3 main.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 