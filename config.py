import os
from datetime import datetime

class AppConfig:
    """Configuration settings for the Bangladeshi Fitness App"""
    
    # App Information
    APP_NAME = "ফিটনেস ট্র্যাকার"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Bangladeshi Fitness and Nutrition Tracker"
    
    # Database Configuration - MySQL
    DATABASE_TYPE = "mysql"
    DATABASE_HOST = os.getenv('DB_HOST', 'localhost')
    DATABASE_PORT = int(os.getenv('DB_PORT', 3306))
    DATABASE_NAME = os.getenv('DB_NAME', 'bangladeshi_fitness')
    DATABASE_USER = os.getenv('DB_USER', 'root')
    DATABASE_PASSWORD = os.getenv('DB_PASSWORD', '')
    DATABASE_CHARSET = 'utf8mb4'
    
    # SQLite fallback (for development)
    SQLITE_DATABASE_NAME = "bangladeshi_fitness.db"
    SQLITE_DATABASE_PATH = os.path.join(os.getcwd(), SQLITE_DATABASE_NAME)
    
    # UI Configuration
    THEME_PRIMARY = "Green"
    THEME_STYLE = "Light"
    WINDOW_SIZE = (400, 700)  # For development
    
    # Language Settings
    DEFAULT_LANGUAGE = "bangla"
    SUPPORTED_LANGUAGES = ["bangla", "english"]
    
    # Calorie Goals (default values)
    DEFAULT_CALORIE_GOAL = 2000
    DEFAULT_WATER_GOAL = 8  # glasses per day
    
    # Activity Levels for TDEE calculation
    ACTIVITY_LEVELS = {
        "sedentary": {
            "bangla": "নিষ্ক্রিয়",
            "english": "Sedentary",
            "description": "Little or no exercise"
        },
        "light": {
            "bangla": "হালকা",
            "english": "Light",
            "description": "Light exercise 1-3 days/week"
        },
        "moderate": {
            "bangla": "মাঝারি",
            "english": "Moderate",
            "description": "Moderate exercise 3-5 days/week"
        },
        "active": {
            "bangla": "সক্রিয়",
            "english": "Active",
            "description": "Hard exercise 6-7 days/week"
        },
        "very_active": {
            "bangla": "অত্যন্ত সক্রিয়",
            "english": "Very Active",
            "description": "Very hard exercise, physical job"
        }
    }
    
    # Fitness Goals
    FITNESS_GOALS = {
        "weight_loss": {
            "bangla": "ওজন কমানো",
            "english": "Weight Loss",
            "calorie_adjustment": -500
        },
        "weight_gain": {
            "bangla": "ওজন বাড়ানো",
            "english": "Weight Gain",
            "calorie_adjustment": 300
        },
        "maintenance": {
            "bangla": "ওজন বজায় রাখা",
            "english": "Maintenance",
            "calorie_adjustment": 0
        }
    }
    
    # Meal Types
    MEAL_TYPES = {
        "breakfast": {
            "bangla": "সকালের নাস্তা",
            "english": "Breakfast"
        },
        "lunch": {
            "bangla": "দুপুরের খাবার",
            "english": "Lunch"
        },
        "dinner": {
            "bangla": "রাতের খাবার",
            "english": "Dinner"
        },
        "snack": {
            "bangla": "নাস্তা",
            "english": "Snack"
        }
    }
    
    # Exercise Categories
    EXERCISE_CATEGORIES = {
        "strength": {
            "bangla": "শক্তি",
            "english": "Strength"
        },
        "cardio": {
            "bangla": "কার্ডিও",
            "english": "Cardio"
        },
        "core": {
            "bangla": "কোর",
            "english": "Core"
        },
        "flexibility": {
            "bangla": "নমনীয়তা",
            "english": "Flexibility"
        }
    }
    
    # Exercise Levels
    EXERCISE_LEVELS = {
        "beginner": {
            "bangla": "শুরুর",
            "english": "Beginner"
        },
        "intermediate": {
            "bangla": "মাঝারি",
            "english": "Intermediate"
        },
        "advanced": {
            "bangla": "উন্নত",
            "english": "Advanced"
        }
    }
    
    # Food Categories
    FOOD_CATEGORIES = {
        "grains": {
            "bangla": "শস্য",
            "english": "Grains"
        },
        "protein": {
            "bangla": "প্রোটিন",
            "english": "Protein"
        },
        "vegetables": {
            "bangla": "সবজি",
            "english": "Vegetables"
        },
        "fruits": {
            "bangla": "ফল",
            "english": "Fruits"
        },
        "dairy": {
            "bangla": "দুগ্ধজাত",
            "english": "Dairy"
        },
        "fats": {
            "bangla": "চর্বি",
            "english": "Fats"
        }
    }
    
    # Notification Settings
    NOTIFICATIONS = {
        "water_reminder": True,
        "meal_reminder": True,
        "exercise_reminder": True,
        "goal_reminder": True
    }
    
    # Data Export Settings
    EXPORT_FORMATS = ["json", "csv", "pdf"]
    
    # Privacy Settings
    PRIVACY = {
        "data_sharing": False,
        "analytics": True,
        "backup_enabled": True
    }
    
    @classmethod
    def get_text(cls, key, language="bangla"):
        """Get localized text for a given key"""
        if hasattr(cls, key.upper()):
            category = getattr(cls, key.upper())
            if isinstance(category, dict) and language in category:
                return category[language]
        return key
    
    @classmethod
    def get_meal_type_text(cls, meal_type, language="bangla"):
        """Get localized meal type text"""
        return cls.MEAL_TYPES.get(meal_type, {}).get(language, meal_type)
    
    @classmethod
    def get_exercise_level_text(cls, level, language="bangla"):
        """Get localized exercise level text"""
        return cls.EXERCISE_LEVELS.get(level, {}).get(language, level)
    
    @classmethod
    def get_food_category_text(cls, category, language="bangla"):
        """Get localized food category text"""
        return cls.FOOD_CATEGORIES.get(category, {}).get(language, category)
    
    @classmethod
    def get_fitness_goal_text(cls, goal, language="bangla"):
        """Get localized fitness goal text"""
        return cls.FITNESS_GOALS.get(goal, {}).get(language, goal)
    
    @classmethod
    def get_activity_level_text(cls, level, language="bangla"):
        """Get localized activity level text"""
        return cls.ACTIVITY_LEVELS.get(level, {}).get(language, level)

class DevelopmentConfig(AppConfig):
    """Development-specific configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    
class ProductionConfig(AppConfig):
    """Production-specific configuration"""
    DEBUG = False
    LOG_LEVEL = "INFO"
    
    # Override window size for mobile
    WINDOW_SIZE = None

# Default configuration
Config = DevelopmentConfig if os.getenv('FLASK_ENV') == 'development' else ProductionConfig 