import mysql.connector
import pymysql
import sqlite3
from datetime import datetime, date
import json
from database import Database
from config import Config

class FitnessUtils:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def calculate_bmr(self, weight, height, age, gender):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if gender.lower() == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        return round(bmr)
    
    def calculate_tdee(self, bmr, activity_level):
        """Calculate Total Daily Energy Expenditure"""
        activity_multipliers = {
            'sedentary': 1.2,      # Little or no exercise
            'light': 1.375,         # Light exercise 1-3 days/week
            'moderate': 1.55,       # Moderate exercise 3-5 days/week
            'active': 1.725,        # Hard exercise 6-7 days/week
            'very_active': 1.9      # Very hard exercise, physical job
        }
        return round(bmr * activity_multipliers.get(activity_level, 1.2))
    
    def get_calorie_goal(self, tdee, goal):
        """Calculate calorie goal based on fitness objective"""
        if goal == 'weight_loss':
            return tdee - 500  # 500 calorie deficit
        elif goal == 'weight_gain':
            return tdee + 300  # 300 calorie surplus
        else:  # maintenance
            return tdee
    
    def get_macro_ratios(self, goal):
        """Get macro ratios based on fitness goal"""
        if goal == 'weight_loss':
            return {'protein': 0.3, 'carbs': 0.4, 'fat': 0.3}
        elif goal == 'weight_gain':
            return {'protein': 0.25, 'carbs': 0.55, 'fat': 0.2}
        else:  # maintenance
            return {'protein': 0.25, 'carbs': 0.5, 'fat': 0.25}
    
    def calculate_macros(self, calories, goal):
        """Calculate macro targets in grams"""
        ratios = self.get_macro_ratios(goal)
        macros = {}
        macros['protein'] = round((calories * ratios['protein']) / 4)  # 4 cal/g
        macros['carbs'] = round((calories * ratios['carbs']) / 4)      # 4 cal/g
        macros['fat'] = round((calories * ratios['fat']) / 9)          # 9 cal/g
        return macros

class BangladeshiFoodData:
    """Database of common Bangladeshi foods with nutritional information"""
    
    @staticmethod
    def get_common_foods():
        """Return common Bangladeshi foods with nutritional data"""
        return [
            {
                'name_bangla': 'ভাত',
                'name_english': 'Rice',
                'calories_per_100g': 130,
                'protein': 2.7,
                'carbs': 28,
                'fat': 0.3,
                'category': 'Grains',
                'serving_size': '1 cup (cooked)',
                'serving_weight': 195
            },
            {
                'name_bangla': 'রুটি',
                'name_english': 'Roti/Chapati',
                'calories_per_100g': 80,
                'protein': 3,
                'carbs': 15,
                'fat': 1,
                'category': 'Grains',
                'serving_size': '1 piece',
                'serving_weight': 30
            },
            {
                'name_bangla': 'মাছ',
                'name_english': 'Fish',
                'calories_per_100g': 120,
                'protein': 20,
                'carbs': 0,
                'fat': 5,
                'category': 'Protein',
                'serving_size': '100g',
                'serving_weight': 100
            },
            {
                'name_bangla': 'মাংস',
                'name_english': 'Meat',
                'calories_per_100g': 250,
                'protein': 25,
                'carbs': 0,
                'fat': 15,
                'category': 'Protein',
                'serving_size': '100g',
                'serving_weight': 100
            },
            {
                'name_bangla': 'ডাল',
                'name_english': 'Lentils',
                'calories_per_100g': 100,
                'protein': 6,
                'carbs': 18,
                'fat': 0.4,
                'category': 'Protein',
                'serving_size': '1/2 cup (cooked)',
                'serving_weight': 100
            },
            {
                'name_bangla': 'সবজি',
                'name_english': 'Vegetables',
                'calories_per_100g': 50,
                'protein': 3,
                'carbs': 10,
                'fat': 0.2,
                'category': 'Vegetables',
                'serving_size': '1 cup',
                'serving_weight': 100
            },
            {
                'name_bangla': 'দুধ',
                'name_english': 'Milk',
                'calories_per_100g': 150,
                'protein': 8,
                'carbs': 12,
                'fat': 8,
                'category': 'Dairy',
                'serving_size': '1 glass',
                'serving_weight': 250
            },
            {
                'name_bangla': 'ডিম',
                'name_english': 'Egg',
                'calories_per_100g': 70,
                'protein': 6,
                'carbs': 1,
                'fat': 5,
                'category': 'Protein',
                'serving_size': '1 egg',
                'serving_weight': 50
            },
            {
                'name_bangla': 'কলা',
                'name_english': 'Banana',
                'calories_per_100g': 105,
                'protein': 1,
                'carbs': 27,
                'fat': 0.4,
                'category': 'Fruits',
                'serving_size': '1 medium',
                'serving_weight': 118
            },
            {
                'name_bangla': 'আপেল',
                'name_english': 'Apple',
                'calories_per_100g': 95,
                'protein': 0.5,
                'carbs': 25,
                'fat': 0.3,
                'category': 'Fruits',
                'serving_size': '1 medium',
                'serving_weight': 182
            },
            {
                'name_bangla': 'আলু',
                'name_english': 'Potato',
                'calories_per_100g': 77,
                'protein': 2,
                'carbs': 17,
                'fat': 0.1,
                'category': 'Vegetables',
                'serving_size': '1 medium',
                'serving_weight': 173
            },
            {
                'name_bangla': 'টমেটো',
                'name_english': 'Tomato',
                'calories_per_100g': 18,
                'protein': 0.9,
                'carbs': 3.9,
                'fat': 0.2,
                'category': 'Vegetables',
                'serving_size': '1 medium',
                'serving_weight': 123
            },
            {
                'name_bangla': 'পেঁয়াজ',
                'name_english': 'Onion',
                'calories_per_100g': 40,
                'protein': 1.1,
                'carbs': 9.3,
                'fat': 0.1,
                'category': 'Vegetables',
                'serving_size': '1 medium',
                'serving_weight': 110
            },
            {
                'name_bangla': 'গাজর',
                'name_english': 'Carrot',
                'calories_per_100g': 41,
                'protein': 0.9,
                'carbs': 9.6,
                'fat': 0.2,
                'category': 'Vegetables',
                'serving_size': '1 medium',
                'serving_weight': 61
            },
            {
                'name_bangla': 'বেগুন',
                'name_english': 'Eggplant',
                'calories_per_100g': 25,
                'protein': 1,
                'carbs': 6,
                'fat': 0.2,
                'category': 'Vegetables',
                'serving_size': '1 cup',
                'serving_weight': 82
            }
        ]

class ExerciseData:
    """Database of exercises with difficulty levels and descriptions"""
    
    @staticmethod
    def get_exercises():
        """Return exercise database with Bangla translations"""
        return [
            {
                'name_bangla': 'পুশ-আপ',
                'name_english': 'Push-ups',
                'level': 'Beginner',
                'category': 'Strength',
                'description': 'বুকের ব্যায়াম - হাতের উপর ভর দিয়ে শরীর উঠানো-নামানো',
                'muscle_groups': ['Chest', 'Triceps', 'Shoulders'],
                'equipment': 'None',
                'instructions': 'পেটের উপর শুয়ে হাতের উপর ভর দিয়ে শরীর উঠান'
            },
            {
                'name_bangla': 'স্কোয়াট',
                'name_english': 'Squats',
                'level': 'Beginner',
                'category': 'Strength',
                'description': 'পায়ের ব্যায়াম - হাঁটু বেঁকিয়ে বসা',
                'muscle_groups': ['Quadriceps', 'Glutes', 'Hamstrings'],
                'equipment': 'None',
                'instructions': 'পা ফাঁক করে দাঁড়িয়ে হাঁটু বেঁকিয়ে বসুন'
            },
            {
                'name_bangla': 'প্লাঙ্ক',
                'name_english': 'Plank',
                'level': 'Intermediate',
                'category': 'Core',
                'description': 'পেটের ব্যায়াম - শরীর সোজা রেখে ধরে রাখা',
                'muscle_groups': ['Core', 'Shoulders', 'Back'],
                'equipment': 'None',
                'instructions': 'কনুই এবং পায়ের আঙুলে ভর দিয়ে শরীর সোজা রাখুন'
            },
            {
                'name_bangla': 'বারপি',
                'name_english': 'Burpees',
                'level': 'Advanced',
                'category': 'Cardio',
                'description': 'পুরো শরীরের ব্যায়াম - স্কোয়াট, পুশ-আপ এবং লাফ',
                'muscle_groups': ['Full Body'],
                'equipment': 'None',
                'instructions': 'স্কোয়াট করে হাত মাটিতে রাখুন, পা পিছনে দিন, পুশ-আপ করুন, লাফ দিন'
            },
            {
                'name_bangla': 'লাঞ্জ',
                'name_english': 'Lunges',
                'level': 'Intermediate',
                'category': 'Strength',
                'description': 'পায়ের ব্যায়াম - এক পা সামনে রেখে বসা',
                'muscle_groups': ['Quadriceps', 'Glutes', 'Hamstrings'],
                'equipment': 'None',
                'instructions': 'এক পা সামনে রেখে হাঁটু বেঁকিয়ে বসুন'
            },
            {
                'name_bangla': 'মাউন্টেন ক্লাইম্বার',
                'name_english': 'Mountain Climber',
                'level': 'Advanced',
                'category': 'Cardio',
                'description': 'পেটের ব্যায়াম - দৌড়ানোর মত পা আনা-নেওয়া',
                'muscle_groups': ['Core', 'Shoulders'],
                'equipment': 'None',
                'instructions': 'প্লাঙ্ক অবস্থায় থেকে পা দ্রুত আনা-নেওয়া করুন'
            },
            {
                'name_bangla': 'ক্রাঞ্চ',
                'name_english': 'Crunches',
                'level': 'Beginner',
                'category': 'Core',
                'description': 'পেটের ব্যায়াম - উপরের শরীর তুলে পেটে চাপ',
                'muscle_groups': ['Abs'],
                'equipment': 'None',
                'instructions': 'শুয়ে হাঁটু বেঁকিয়ে উপরের শরীর তুলুন'
            },
            {
                'name_bangla': 'জাম্পিং জ্যাক',
                'name_english': 'Jumping Jacks',
                'level': 'Beginner',
                'category': 'Cardio',
                'description': 'কার্ডিও ব্যায়াম - লাফিয়ে হাত-পা ছড়ানো',
                'muscle_groups': ['Full Body'],
                'equipment': 'None',
                'instructions': 'লাফিয়ে হাত-পা ছড়ান এবং আবার একত্র করুন'
            },
            {
                'name_bangla': 'সাইড প্লাঙ্ক',
                'name_english': 'Side Plank',
                'level': 'Intermediate',
                'category': 'Core',
                'description': 'পেটের পার্শ্বীয় ব্যায়াম - এক পাশে ভর দিয়ে ধরে রাখা',
                'muscle_groups': ['Obliques', 'Shoulders'],
                'equipment': 'None',
                'instructions': 'এক কনুইতে ভর দিয়ে শরীর সোজা রাখুন'
            },
            {
                'name_bangla': 'ওয়াল সিট',
                'name_english': 'Wall Sit',
                'level': 'Beginner',
                'category': 'Strength',
                'description': 'পায়ের ব্যায়াম - দেওয়ালে ভর দিয়ে বসা',
                'muscle_groups': ['Quadriceps', 'Glutes'],
                'equipment': 'Wall',
                'instructions': 'দেওয়ালে পিঠ লাগিয়ে স্কোয়াট অবস্থায় বসুন'
            }
        ]

class DataManager:
    """Manages data operations for the fitness app"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.utils = FitnessUtils(db_connection)
    
    def add_food_log(self, user_id, food_name, amount, meal_type, date=None):
        """Add food to user's daily log"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Get food info from database
        food = self.db.fetch_one('''
            SELECT id, calories_per_100g FROM foods 
            WHERE name_bangla = %s OR name_english = %s
        ''', (food_name, food_name))
        
        if food:
            food_id, calories_per_100g = food
            total_calories = (calories_per_100g * amount) / 100
            
            self.db.insert('''
                INSERT INTO food_logs (user_id, food_id, amount, date, meal_type)
                VALUES (%s, %s, %s, %s, %s)
            ''', (user_id, food_id, amount, date, meal_type))
            
            return total_calories
        return 0
    
    def get_daily_calories(self, user_id, date=None):
        """Get total calories consumed on a specific date"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        result = self.db.fetch_one('''
            SELECT SUM(f.calories_per_100g * fl.amount / 100)
            FROM food_logs fl
            JOIN foods f ON fl.food_id = f.id
            WHERE fl.user_id = %s AND fl.date = %s
        ''', (user_id, date))
        
        return result[0] if result and result[0] else 0
    
    def get_meal_logs(self, user_id, date=None):
        """Get all meals logged for a specific date"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        return self.db.fetch_all('''
            SELECT f.name_bangla, fl.amount, fl.meal_type, 
                   (f.calories_per_100g * fl.amount / 100) as calories
            FROM food_logs fl
            JOIN foods f ON fl.food_id = f.id
            WHERE fl.user_id = %s AND fl.date = %s
            ORDER BY fl.meal_type
        ''', (user_id, date))
    
    def add_exercise_log(self, user_id, exercise_name, duration, sets=0, reps=0, date=None):
        """Add exercise to user's daily log"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Get exercise info from database
        exercise = self.db.fetch_one('''
            SELECT id FROM exercises 
            WHERE name_bangla = %s OR name_english = %s
        ''', (exercise_name, exercise_name))
        
        if exercise:
            exercise_id = exercise[0]
            
            self.db.insert('''
                INSERT INTO exercise_logs (user_id, exercise_id, duration, sets, reps, date)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (user_id, exercise_id, duration, sets, reps, date))
            
            return True
        return False
    
    def get_exercise_logs(self, user_id, date=None):
        """Get all exercises logged for a specific date"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        return self.db.fetch_all('''
            SELECT e.name_bangla, el.duration, el.sets, el.reps
            FROM exercise_logs el
            JOIN exercises e ON el.exercise_id = e.id
            WHERE el.user_id = %s AND el.date = %s
            ORDER BY el.duration DESC
        ''', (user_id, date))
    
    def add_to_pantry(self, user_id, food_name, custom_name=None, custom_calories=None):
        """Add food item to user's pantry"""
        # Get food info from database
        food = self.db.fetch_one('''
            SELECT id FROM foods 
            WHERE name_bangla = %s OR name_english = %s
        ''', (food_name, food_name))
        
        if food:
            food_id = food[0]
            
            self.db.insert('''
                INSERT INTO pantry (user_id, food_id, custom_name, custom_calories)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                custom_name = VALUES(custom_name),
                custom_calories = VALUES(custom_calories)
            ''', (user_id, food_id, custom_name, custom_calories))
            
            return True
        return False
    
    def get_pantry_items(self, user_id):
        """Get all items in user's pantry"""
        return self.db.fetch_all('''
            SELECT f.name_bangla, f.calories_per_100g, p.custom_name, p.custom_calories
            FROM pantry p
            JOIN foods f ON p.food_id = f.id
            WHERE p.user_id = %s
        ''', (user_id,))
    
    def add_water_log(self, user_id, glasses=1, date=None):
        """Add water intake to user's daily log"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        self.db.insert('''
            INSERT INTO water_logs (user_id, glasses, date)
            VALUES (%s, %s, %s)
        ''', (user_id, glasses, date))
        
        return True
    
    def get_daily_water(self, user_id, date=None):
        """Get total water consumed on a specific date"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        result = self.db.fetch_one('''
            SELECT SUM(glasses)
            FROM water_logs
            WHERE user_id = %s AND date = %s
        ''', (user_id, date))
        
        return result[0] if result and result[0] else 0 