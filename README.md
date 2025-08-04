# 🏃‍♂️ Bangladeshi Fitness App

A comprehensive fitness tracking application designed specifically for the Bangladeshi community, featuring Bengali language support and culturally relevant food and exercise options.

## 🌟 Features

### 🌐 **Bilingual Support**
- **Language Toggle**: Switch between Bengali and English
- **Complete Translation**: All interface elements in both languages
- **Font Adaptation**: Bengali (Noto Sans Bengali) and English (Inter) fonts
- **Session Persistence**: Language preference saved during session

### 📊 Dashboard
- **Daily Summary**: Track calories, water intake, and exercise
- **Progress Visualization**: Beautiful charts and progress bars
- **Quick Actions**: Easy access to add food, exercise, and water
- **Recent Activities**: View today's logged activities

### 🍽️ Food Tracking
- **Bangladeshi Foods**: Pre-loaded with common Bangladeshi foods
- **Nutritional Info**: Calories, protein, carbs, and fat tracking
- **Custom Foods**: Add your own foods to the database
- **Meal Categorization**: Breakfast, lunch, dinner, snacks

### 💪 Exercise Tracking
- **Multiple Levels**: Beginner, Intermediate, Advanced exercises
- **Exercise Categories**: Strength, Cardio, Core training
- **Duration & Sets**: Track time, sets, and repetitions
- **Bangladeshi Context**: Exercises suitable for home workouts

### 🏠 Pantry Management
- **Personal Pantry**: Save your frequently used foods
- **Quick Access**: Easy food logging from your pantry
- **Custom Items**: Add homemade or custom foods

### 👤 Profile Management
- **Personal Goals**: Weight loss, gain, or maintenance
- **Body Metrics**: Track weight, height, age
- **Target Setting**: Customize calorie and water goals
- **Progress Tracking**: Monitor your fitness journey

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip3 (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd /path/to/projects
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the web application**
   ```bash
   python3 run_web_app.py
   ```
   
   Or run directly:
   ```bash
   python3 web_app.py
   ```

4. **Open your browser**
   - The app will automatically open at: http://localhost:8080
   - Or manually navigate to: http://localhost:8080

## 📱 Using the App

### 🏠 Dashboard
- **View your daily summary** with calories and water intake
- **Quick actions** to add food, exercise, or water
- **Recent activities** showing today's logged items
- **Progress bars** for calorie and water goals

### 🍽️ Adding Food
1. Navigate to the "খাবার" (Food) or "Food" tab
2. **Search** for foods or browse categories
3. **Quick add** common Bangladeshi foods
4. **Custom foods** can be added with nutritional info
5. **Select amount** and meal type
6. **Submit** to log your food

### 💪 Adding Exercise
1. Go to the "ব্যায়াম" (Exercise) or "Exercise" tab
2. **Filter by level** (Beginner/Intermediate/Advanced)
3. **Browse exercise categories** (Strength/Cardio/Core)
4. **Select an exercise** and enter details
5. **Log duration, sets, and reps**
6. **Submit** to track your workout

### 🏠 Managing Pantry
1. Visit the "প্যান্ট্রি" (Pantry) or "Pantry" tab
2. **Add foods** to your personal pantry
3. **Quick access** to frequently used items
4. **Custom foods** for homemade meals

### 👤 Profile Settings
1. Access the "প্রোফাইল" (Profile) or "Profile" tab
2. **Update personal information**
3. **Set fitness goals**
4. **Adjust calorie targets**
5. **View progress statistics**

## 🗄️ Database

The app uses SQLite for data storage:
- **Automatic setup**: Database is created on first run
- **Sample data**: Pre-loaded with common Bangladeshi foods
- **User data**: Personal logs and preferences
- **Backup**: Data is stored locally in `fitness_demo.db`

## 🛠️ Technical Details

### Web Application (Flask)
- **Framework**: Flask with SQLAlchemy
- **Database**: SQLite with ORM
- **Templates**: Jinja2 with Bootstrap 5
- **Styling**: Custom CSS with dark theme and bilingual fonts
- **Language**: Session-based language switching
- **Port**: 8080 (configurable)

### Mobile Application (Kivy)
- **Framework**: Kivy with KivyMD
- **Cross-platform**: Works on Android, iOS, desktop
- **UI**: Material Design components
- **Language**: Bengali interface

## 🎨 Design Features

### 🌐 Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Bilingual Typography**: Noto Sans Bengali for Bengali, Inter for English
- **Modern UI**: Bootstrap 5 with custom dark theme styling
- **Color Scheme**: Dark neutral theme with red, green, and blue accents
- **Smooth Animations**: Hover effects and transitions
- **Language Toggle**: Easy switching between Bengali and English

### 🎨 **Dark Theme Colors**
- **Background**: Dark neutral grays (#1a1a1a, #2d2d2d, #3a3a3a)
- **Text**: White and light gray for readability
- **Accents**: Red (#e74c3c), Green (#27ae60), Blue (#3498db)
- **Neutral Palette**: Full range of grays for UI elements
- **Gradient Effects**: Subtle gradients for depth and visual interest

### 📱 Mobile Interface
- **Native Feel**: KivyMD Material Design components
- **Touch Optimized**: Large buttons and easy navigation
- **Offline Capable**: Works without internet connection
- **Cross-platform**: Same codebase for all platforms

## 🍽️ Bangladeshi Foods Included

### Grains & Breads
- ভাত (Rice) - 130 calories/100g
- রুটি (Roti) - 80 calories/100g

### Proteins
- মাছ (Fish) - 120 calories/100g
- মাংস (Meat) - 250 calories/100g
- ডাল (Lentils) - 100 calories/100g
- ডিম (Egg) - 70 calories/100g

### Dairy
- দুধ (Milk) - 150 calories/100g

### Fruits & Vegetables
- সবজি (Vegetables) - 50 calories/100g
- কলা (Banana) - 105 calories/100g
- আপেল (Apple) - 95 calories/100g

## 💪 Exercise Categories

### Beginner Level
- পুশ-আপ (Push-ups)
- স্কোয়াট (Squats)

### Intermediate Level
- প্লাঙ্ক (Plank)
- লাঞ্জ (Lunges)

### Advanced Level
- বারপি (Burpees)
- মাউন্টেন ক্লাইম্বার (Mountain Climber)

## 🔧 Troubleshooting

### Port Already in Use
If you get "Address already in use" error:
```bash
# On macOS, disable AirPlay Receiver:
# System Preferences → General → AirDrop & Handoff → AirPlay Receiver

# Or use a different port by editing web_app.py:
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Missing Dependencies
```bash
pip3 install -r requirements.txt
```

### Database Issues
```bash
# Delete the database file to reset:
rm fitness_demo.db
# Then restart the app
```

## 📊 Sample Data

The app comes pre-loaded with:
- **1 Demo User**: আহমেদ (Ahmed) - 25 years old, 70kg
- **10 Common Foods**: Bangladeshi staples with nutritional info
- **6 Exercises**: Different difficulty levels
- **Sample Logs**: Example food and exercise entries

## 🎯 Future Enhancements

- [ ] **Social Features**: Share progress with friends
- [ ] **Recipe Database**: Traditional Bangladeshi recipes
- [ ] **Workout Plans**: Pre-made exercise routines
- [ ] **Progress Charts**: Long-term trend analysis
- [ ] **Export Data**: Backup and share functionality
- [ ] **Notifications**: Reminders for meals and exercise
- [ ] **Offline Mode**: Enhanced mobile functionality

## 🤝 Contributing

This app is designed for the Bangladeshi fitness community. Contributions are welcome:
- Add more Bangladeshi foods
- Include traditional exercises
- Improve Bengali translations
- Enhance UI/UX for local users

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ for the Bangladeshi fitness community**

*ফিটনেস ট্র্যাকার - আপনার স্বাস্থ্য, আমাদের লক্ষ্য* 