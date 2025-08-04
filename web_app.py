from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bangladeshi_fitness_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    goal = db.Column(db.String(50))
    target_calories = db.Column(db.Integer, default=2000)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_bangla = db.Column(db.String(100))
    name_english = db.Column(db.String(100))
    calories_per_100g = db.Column(db.Integer)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    category = db.Column(db.String(50))
    serving_size = db.Column(db.String(100))
    serving_weight = db.Column(db.Float)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_bangla = db.Column(db.String(100))
    name_english = db.Column(db.String(100))
    level = db.Column(db.String(50))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)

class FoodLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    amount = db.Column(db.Float)
    date = db.Column(db.Date, default=date.today)
    meal_type = db.Column(db.String(50))

class ExerciseLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    duration = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    date = db.Column(db.Date, default=date.today)

class Pantry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    custom_name = db.Column(db.String(100))
    custom_calories = db.Column(db.Integer)

class WaterLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    glasses = db.Column(db.Integer, default=1)
    date = db.Column(db.Date, default=date.today)

# Sample data
def insert_sample_data():
    # Sample foods
    foods = [
        Food(name_bangla='ভাত', name_english='Rice', calories_per_100g=130, protein=2.7, carbs=28, fat=0.3, category='Grains', serving_size='1 cup (cooked)', serving_weight=195),
        Food(name_bangla='রুটি', name_english='Roti', calories_per_100g=80, protein=3, carbs=15, fat=1, category='Grains', serving_size='1 piece', serving_weight=30),
        Food(name_bangla='মাছ', name_english='Fish', calories_per_100g=120, protein=20, carbs=0, fat=5, category='Protein', serving_size='100g', serving_weight=100),
        Food(name_bangla='মাংস', name_english='Meat', calories_per_100g=250, protein=25, carbs=0, fat=15, category='Protein', serving_size='100g', serving_weight=100),
        Food(name_bangla='ডাল', name_english='Lentils', calories_per_100g=100, protein=6, carbs=18, fat=0.4, category='Protein', serving_size='1/2 cup (cooked)', serving_weight=100),
        Food(name_bangla='সবজি', name_english='Vegetables', calories_per_100g=50, protein=3, carbs=10, fat=0.2, category='Vegetables', serving_size='1 cup', serving_weight=100),
        Food(name_bangla='দুধ', name_english='Milk', calories_per_100g=150, protein=8, carbs=12, fat=8, category='Dairy', serving_size='1 glass', serving_weight=250),
        Food(name_bangla='ডিম', name_english='Egg', calories_per_100g=70, protein=6, carbs=1, fat=5, category='Protein', serving_size='1 egg', serving_weight=50),
        Food(name_bangla='কলা', name_english='Banana', calories_per_100g=105, protein=1, carbs=27, fat=0.4, category='Fruits', serving_size='1 medium', serving_weight=118),
        Food(name_bangla='আপেল', name_english='Apple', calories_per_100g=95, protein=0.5, carbs=25, fat=0.3, category='Fruits', serving_size='1 medium', serving_weight=182)
    ]
    
    # Sample exercises
    exercises = [
        Exercise(name_bangla='পুশ-আপ', name_english='Push-ups', level='Beginner', category='Strength', description='বুকের ব্যায়াম - হাতের উপর ভর দিয়ে শরীর উঠানো-নামানো'),
        Exercise(name_bangla='স্কোয়াট', name_english='Squats', level='Beginner', category='Strength', description='পায়ের ব্যায়াম - হাঁটু বেঁকিয়ে বসা'),
        Exercise(name_bangla='প্লাঙ্ক', name_english='Plank', level='Intermediate', category='Core', description='পেটের ব্যায়াম - শরীর সোজা রেখে ধরে রাখা'),
        Exercise(name_bangla='বারপি', name_english='Burpees', level='Advanced', category='Cardio', description='পুরো শরীরের ব্যায়াম - স্কোয়াট, পুশ-আপ এবং লাফ'),
        Exercise(name_bangla='লাঞ্জ', name_english='Lunges', level='Intermediate', category='Strength', description='পায়ের ব্যায়াম - এক পা সামনে রেখে বসা'),
        Exercise(name_bangla='মাউন্টেন ক্লাইম্বার', name_english='Mountain Climber', level='Advanced', category='Cardio', description='পেটের ব্যায়াম - দৌড়ানোর মত পা আনা-নেওয়া')
    ]
    
    for food in foods:
        db.session.add(food)
    
    for exercise in exercises:
        db.session.add(exercise)
    
    # Create demo user
    demo_user = User(name='আহমেদ', age=25, weight=70, height=170, goal='weight_loss', target_calories=2000)
    db.session.add(demo_user)
    
    db.session.commit()

# Routes
@app.route('/')
def dashboard():
    user = User.query.first()
    if not user:
        user = User(name='আহমেদ', age=25, weight=70, height=170, goal='weight_loss', target_calories=2000)
        db.session.add(user)
        db.session.commit()
    
    # Get today's logs
    today = date.today()
    food_logs = FoodLog.query.filter_by(user_id=user.id, date=today).all()
    exercise_logs = ExerciseLog.query.filter_by(user_id=user.id, date=today).all()
    water_logs = WaterLog.query.filter_by(user_id=user.id, date=today).all()
    
    # Calculate totals
    total_calories = sum(log.amount * Food.query.get(log.food_id).calories_per_100g / 100 for log in food_logs)
    total_water = sum(log.glasses for log in water_logs)
    
    # Get related objects for template
    for log in food_logs:
        log.food = Food.query.get(log.food_id)
    
    for log in exercise_logs:
        log.exercise = Exercise.query.get(log.exercise_id)
    
    return render_template('dashboard.html', 
                         user=user, 
                         food_logs=food_logs,
                         exercise_logs=exercise_logs,
                         water_logs=water_logs,
                         total_calories=total_calories,
                         total_water=total_water)

@app.route('/food')
def food_tracking():
    foods = Food.query.all()
    categories = db.session.query(Food.category).distinct().all()
    return render_template('food.html', foods=foods, categories=categories)

@app.route('/exercise')
def exercise_tracking():
    exercises = Exercise.query.all()
    levels = db.session.query(Exercise.level).distinct().all()
    categories = db.session.query(Exercise.category).distinct().all()
    return render_template('exercise.html', exercises=exercises, levels=levels, categories=categories)

@app.route('/pantry')
def pantry():
    user = User.query.first()
    pantry_items = Pantry.query.filter_by(user_id=user.id).all()
    foods = Food.query.all()
    return render_template('pantry.html', pantry_items=pantry_items, foods=foods)

@app.route('/profile')
def profile():
    user = User.query.first()
    return render_template('profile.html', user=user)

@app.route('/add_food', methods=['POST'])
def add_food():
    user = User.query.first()
    food_id = request.form.get('food_id')
    amount = float(request.form.get('amount', 100))
    meal_type = request.form.get('meal_type', 'snack')
    
    food_log = FoodLog(user_id=user.id, food_id=food_id, amount=amount, meal_type=meal_type)
    db.session.add(food_log)
    db.session.commit()
    
    flash('খাবার যোগ করা হয়েছে!' if session.get('language', 'bn') == 'bn' else 'Food added successfully!', 'success')
    return redirect(url_for('food_tracking'))

@app.route('/add_exercise', methods=['POST'])
def add_exercise():
    user = User.query.first()
    exercise_id = request.form.get('exercise_id')
    duration = int(request.form.get('duration', 10))
    sets = int(request.form.get('sets', 0))
    reps = int(request.form.get('reps', 0))
    
    exercise_log = ExerciseLog(user_id=user.id, exercise_id=exercise_id, duration=duration, sets=sets, reps=reps)
    db.session.add(exercise_log)
    db.session.commit()
    
    flash('ব্যায়াম যোগ করা হয়েছে!' if session.get('language', 'bn') == 'bn' else 'Exercise added successfully!', 'success')
    return redirect(url_for('exercise_tracking'))

@app.route('/add_water', methods=['POST'])
def add_water():
    user = User.query.first()
    glasses = int(request.form.get('glasses', 1))
    
    water_log = WaterLog(user_id=user.id, glasses=glasses)
    db.session.add(water_log)
    db.session.commit()
    
    flash('পানি যোগ করা হয়েছে!' if session.get('language', 'bn') == 'bn' else 'Water added successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/add_to_pantry', methods=['POST'])
def add_to_pantry():
    user = User.query.first()
    food_id = request.form.get('food_id')
    custom_name = request.form.get('custom_name', '')
    
    pantry_item = Pantry(user_id=user.id, food_id=food_id, custom_name=custom_name)
    db.session.add(pantry_item)
    db.session.commit()
    
    flash('প্যান্ট্রিতে যোগ করা হয়েছে!' if session.get('language', 'bn') == 'bn' else 'Added to pantry!', 'success')
    return redirect(url_for('pantry'))

@app.route('/toggle_language')
def toggle_language():
    current_lang = session.get('language', 'bn')
    new_lang = 'en' if current_lang == 'bn' else 'bn'
    session['language'] = new_lang
    return redirect(request.referrer or url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Food.query.first():
            insert_sample_data()
    
    print("🚀 Bangladeshi Fitness App Web Demo")
    print("🌐 Server running at: http://localhost:8080")
    print("📱 Open your browser to see the app!")
    
    app.run(debug=True, host='0.0.0.0', port=8080) 