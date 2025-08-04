import mysql.connector
import pymysql
import sqlite3
import os
from config import Config
from typing import Optional, Dict, List, Any

class DatabaseManager:
    """Database manager for MySQL and SQLite connections"""
    
    def __init__(self, database_type: str = None):
        self.database_type = database_type or Config.DATABASE_TYPE
        self.connection = None
        
    def get_connection(self):
        """Get database connection based on type"""
        if self.database_type == "mysql":
            return self._get_mysql_connection()
        else:
            return self._get_sqlite_connection()
    
    def _get_mysql_connection(self):
        """Get MySQL connection"""
        try:
            connection = mysql.connector.connect(
                host=Config.DATABASE_HOST,
                port=Config.DATABASE_PORT,
                user=Config.DATABASE_USER,
                password=Config.DATABASE_PASSWORD,
                database=Config.DATABASE_NAME,
                charset=Config.DATABASE_CHARSET,
                autocommit=True
            )
            return connection
        except mysql.connector.Error as err:
            print(f"MySQL Connection Error: {err}")
            # Fallback to SQLite if MySQL is not available
            print("Falling back to SQLite...")
            return self._get_sqlite_connection()
    
    def _get_sqlite_connection(self):
        """Get SQLite connection"""
        return sqlite3.connect(Config.SQLITE_DATABASE_PATH)
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

class Database:
    """Main database class for the fitness app"""
    
    def __init__(self, database_type: str = None):
        self.db_manager = DatabaseManager(database_type)
        self.connection = self.db_manager.get_connection()
        self.create_tables()
    
    def create_tables(self):
        """Create database tables"""
        cursor = self.connection.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age INT,
                weight DECIMAL(5,2),
                height DECIMAL(5,2),
                goal VARCHAR(50),
                target_calories INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        
        # Foods table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS foods (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name_bangla VARCHAR(255) NOT NULL,
                name_english VARCHAR(255) NOT NULL,
                calories_per_100g INT NOT NULL,
                protein DECIMAL(5,2),
                carbs DECIMAL(5,2),
                fat DECIMAL(5,2),
                category VARCHAR(50),
                serving_size VARCHAR(100),
                serving_weight DECIMAL(5,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Exercises table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercises (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name_bangla VARCHAR(255) NOT NULL,
                name_english VARCHAR(255) NOT NULL,
                level VARCHAR(50),
                category VARCHAR(50),
                description TEXT,
                muscle_groups TEXT,
                equipment VARCHAR(100),
                instructions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Food logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS food_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                food_id INT,
                amount DECIMAL(8,2),
                date DATE,
                meal_type VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE
            )
        ''')
        
        # Exercise logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercise_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                exercise_id INT,
                duration INT,
                sets INT,
                reps INT,
                date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
            )
        ''')
        
        # Pantry table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pantry (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                food_id INT,
                custom_name VARCHAR(255),
                custom_calories INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE
            )
        ''')
        
        # Water logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS water_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                glasses INT DEFAULT 1,
                date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        self.connection.commit()
        self.insert_sample_data()
    
    def insert_sample_data(self):
        """Insert sample data into the database"""
        cursor = self.connection.cursor()
        
        # Sample Bangladeshi foods
        foods = [
            ("ভাত", "Rice", 130, 2.7, 28, 0.3, "Grains", "1 cup (cooked)", 195),
            ("রুটি", "Roti", 80, 3, 15, 1, "Grains", "1 piece", 30),
            ("মাছ", "Fish", 120, 20, 0, 5, "Protein", "100g", 100),
            ("মাংস", "Meat", 250, 25, 0, 15, "Protein", "100g", 100),
            ("ডাল", "Dal", 100, 6, 18, 0.4, "Protein", "1/2 cup (cooked)", 100),
            ("সবজি", "Vegetables", 50, 3, 10, 0.2, "Vegetables", "1 cup", 100),
            ("দুধ", "Milk", 150, 8, 12, 8, "Dairy", "1 glass", 250),
            ("ডিম", "Egg", 70, 6, 1, 5, "Protein", "1 egg", 50),
            ("কলা", "Banana", 105, 1, 27, 0.4, "Fruits", "1 medium", 118),
            ("আপেল", "Apple", 95, 0.5, 25, 0.3, "Fruits", "1 medium", 182),
            ("আলু", "Potato", 77, 2, 17, 0.1, "Vegetables", "1 medium", 173),
            ("টমেটো", "Tomato", 18, 0.9, 3.9, 0.2, "Vegetables", "1 medium", 123),
            ("পেঁয়াজ", "Onion", 40, 1.1, 9.3, 0.1, "Vegetables", "1 medium", 110),
            ("গাজর", "Carrot", 41, 0.9, 9.6, 0.2, "Vegetables", "1 medium", 61),
            ("বেগুন", "Eggplant", 25, 1, 6, 0.2, "Vegetables", "1 cup", 82)
        ]
        
        for food in foods:
            cursor.execute('''
                INSERT IGNORE INTO foods 
                (name_bangla, name_english, calories_per_100g, protein, carbs, fat, category, serving_size, serving_weight)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', food)
        
        # Sample exercises
        exercises = [
            ("পুশ-আপ", "Push-ups", "Beginner", "Strength", "বুকের ব্যায়াম - হাতের উপর ভর দিয়ে শরীর উঠানো-নামানো", "Chest, Triceps, Shoulders", "None", "পেটের উপর শুয়ে হাতের উপর ভর দিয়ে শরীর উঠান"),
            ("স্কোয়াট", "Squats", "Beginner", "Strength", "পায়ের ব্যায়াম - হাঁটু বেঁকিয়ে বসা", "Quadriceps, Glutes, Hamstrings", "None", "পা ফাঁক করে দাঁড়িয়ে হাঁটু বেঁকিয়ে বসুন"),
            ("প্লাঙ্ক", "Plank", "Intermediate", "Core", "পেটের ব্যায়াম - শরীর সোজা রেখে ধরে রাখা", "Core, Shoulders, Back", "None", "কনুই এবং পায়ের আঙুলে ভর দিয়ে শরীর সোজা রাখুন"),
            ("বারপি", "Burpees", "Advanced", "Cardio", "পুরো শরীরের ব্যায়াম - স্কোয়াট, পুশ-আপ এবং লাফ", "Full Body", "None", "স্কোয়াট করে হাত মাটিতে রাখুন, পা পিছনে দিন, পুশ-আপ করুন, লাফ দিন"),
            ("লাঞ্জ", "Lunges", "Intermediate", "Strength", "পায়ের ব্যায়াম - এক পা সামনে রেখে বসা", "Quadriceps, Glutes, Hamstrings", "None", "এক পা সামনে রেখে হাঁটু বেঁকিয়ে বসুন"),
            ("মাউন্টেন ক্লাইম্বার", "Mountain Climber", "Advanced", "Cardio", "পেটের ব্যায়াম - দৌড়ানোর মত পা আনা-নেওয়া", "Core, Shoulders", "None", "প্লাঙ্ক অবস্থায় থেকে পা দ্রুত আনা-নেওয়া করুন"),
            ("ক্রাঞ্চ", "Crunches", "Beginner", "Core", "পেটের ব্যায়াম - উপরের শরীর তুলে পেটে চাপ", "Abs", "None", "শুয়ে হাঁটু বেঁকিয়ে উপরের শরীর তুলুন"),
            ("জাম্পিং জ্যাক", "Jumping Jacks", "Beginner", "Cardio", "কার্ডিও ব্যায়াম - লাফিয়ে হাত-পা ছড়ানো", "Full Body", "None", "লাফিয়ে হাত-পা ছড়ান এবং আবার একত্র করুন"),
            ("সাইড প্লাঙ্ক", "Side Plank", "Intermediate", "Core", "পেটের পার্শ্বীয় ব্যায়াম - এক পাশে ভর দিয়ে ধরে রাখা", "Obliques, Shoulders", "None", "এক কনুইতে ভর দিয়ে শরীর সোজা রাখুন"),
            ("ওয়াল সিট", "Wall Sit", "Beginner", "Strength", "পায়ের ব্যায়াম - দেওয়ালে ভর দিয়ে বসা", "Quadriceps, Glutes", "Wall", "দেওয়ালে পিঠ লাগিয়ে স্কোয়াট অবস্থায় বসুন")
        ]
        
        for exercise in exercises:
            cursor.execute('''
                INSERT IGNORE INTO exercises 
                (name_bangla, name_english, level, category, description, muscle_groups, equipment, instructions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', exercise)
        
        self.connection.commit()
    
    def execute_query(self, query: str, params: tuple = None):
        """Execute a database query"""
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except Exception as e:
            print(f"Database query error: {e}")
            self.connection.rollback()
            raise e
    
    def fetch_one(self, query: str, params: tuple = None):
        """Fetch one row from database"""
        cursor = self.execute_query(query, params)
        return cursor.fetchone()
    
    def fetch_all(self, query: str, params: tuple = None):
        """Fetch all rows from database"""
        cursor = self.execute_query(query, params)
        return cursor.fetchall()
    
    def insert(self, query: str, params: tuple = None):
        """Insert data into database"""
        cursor = self.execute_query(query, params)
        self.connection.commit()
        return cursor.lastrowid
    
    def update(self, query: str, params: tuple = None):
        """Update data in database"""
        cursor = self.execute_query(query, params)
        self.connection.commit()
        return cursor.rowcount
    
    def delete(self, query: str, params: tuple = None):
        """Delete data from database"""
        cursor = self.execute_query(query, params)
        self.connection.commit()
        return cursor.rowcount
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close() 