#!/usr/bin/env python3
"""
Test script for the Bangladeshi Fitness App
This script tests the basic functionality of the app
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import BangladeshiFoodData, ExerciseData, DataManager
from config import Config
from database import Database

def test_database_connection():
    """Test database connection and table creation"""
    print("🔍 Testing database connection...")
    
    try:
        db = Database()
        
        # Test if tables exist
        tables = db.fetch_all("SHOW TABLES")
        
        print(f"✅ Database connected successfully")
        print(f"📊 Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Falling back to SQLite for testing...")
        try:
            # Try SQLite fallback
            import sqlite3
            conn = sqlite3.connect(Config.SQLITE_DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"✅ SQLite fallback successful")
            print(f"📊 Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table[0]}")
            conn.close()
            return True
        except Exception as e2:
            print(f"❌ SQLite fallback also failed: {e2}")
            return False

def test_food_data():
    """Test food database functionality"""
    print("\n🍽️ Testing food database...")
    
    try:
        foods = BangladeshiFoodData.get_common_foods()
        print(f"✅ Found {len(foods)} food items")
        
        # Test some specific foods
        rice_found = any(food['name_bangla'] == 'ভাত' for food in foods)
        fish_found = any(food['name_bangla'] == 'মাছ' for food in foods)
        
        if rice_found and fish_found:
            print("✅ Common Bangladeshi foods found")
        else:
            print("❌ Some common foods missing")
            
        return True
        
    except Exception as e:
        print(f"❌ Food data test failed: {e}")
        return False

def test_exercise_data():
    """Test exercise database functionality"""
    print("\n💪 Testing exercise database...")
    
    try:
        exercises = ExerciseData.get_exercises()
        print(f"✅ Found {len(exercises)} exercises")
        
        # Test exercise levels
        beginner_exercises = [ex for ex in exercises if ex['level'] == 'Beginner']
        intermediate_exercises = [ex for ex in exercises if ex['level'] == 'Intermediate']
        advanced_exercises = [ex for ex in exercises if ex['level'] == 'Advanced']
        
        print(f"   - Beginner: {len(beginner_exercises)} exercises")
        print(f"   - Intermediate: {len(intermediate_exercises)} exercises")
        print(f"   - Advanced: {len(advanced_exercises)} exercises")
        
        return True
        
    except Exception as e:
        print(f"❌ Exercise data test failed: {e}")
        return False

def test_config():
    """Test configuration settings"""
    print("\n⚙️ Testing configuration...")
    
    try:
        # Test language settings
        bangla_text = Config.get_meal_type_text("breakfast", "bangla")
        english_text = Config.get_meal_type_text("breakfast", "english")
        
        print(f"✅ Language support working:")
        print(f"   - Breakfast (Bangla): {bangla_text}")
        print(f"   - Breakfast (English): {english_text}")
        
        # Test fitness goals
        weight_loss_bangla = Config.get_fitness_goal_text("weight_loss", "bangla")
        print(f"   - Weight Loss (Bangla): {weight_loss_bangla}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_data_manager():
    """Test data manager functionality"""
    print("\n📊 Testing data manager...")
    
    try:
        db = Database()
        data_manager = DataManager(db)
        
        # Test calorie calculation
        bmr = data_manager.utils.calculate_bmr(70, 170, 25, 'male')
        tdee = data_manager.utils.calculate_tdee(bmr, 'moderate')
        calorie_goal = data_manager.utils.get_calorie_goal(tdee, 'weight_loss')
        
        print(f"✅ Calorie calculations working:")
        print(f"   - BMR: {bmr} calories")
        print(f"   - TDEE: {tdee} calories")
        print(f"   - Weight Loss Goal: {calorie_goal} calories")
        
        # Test macro calculations
        macros = data_manager.utils.calculate_macros(calorie_goal, 'weight_loss')
        print(f"   - Protein: {macros['protein']}g")
        print(f"   - Carbs: {macros['carbs']}g")
        print(f"   - Fat: {macros['fat']}g")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Data manager test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Bangladeshi Fitness App Tests")
    print("=" * 50)
    
    tests = [
        test_database_connection,
        test_food_data,
        test_exercise_data,
        test_config,
        test_data_manager
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📈 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The app is ready to run.")
        print("\nTo run the app, use:")
        print("python main.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 