from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.chip import MDChip
# from kivymd.uix.iconbutton import MDIconButton
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
import json
from datetime import datetime, date
import os
from database import Database

# Set window size for development (remove for mobile)
Window.size = (400, 700)

class BangladeshiFitnessApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "ফিটনেস ট্র্যাকার"  # Fitness Tracker in Bangla
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        self.db = Database()
        
    def build(self):
        # Create screen manager
        self.sm = MDScreenManager()
        
        # Create main screen with bottom navigation
        main_screen = MDScreen()
        
        # Create bottom navigation
        bottom_nav = MDBottomNavigation()
        
        # Dashboard Tab
        dashboard_tab = MDBottomNavigationItem(
            name="dashboard",
            text="হোম",  # Home
            icon="home"
        )
        dashboard_tab.add_widget(DashboardScreen())
        
        # Food Tracking Tab
        food_tab = MDBottomNavigationItem(
            name="food",
            text="খাবার",  # Food
            icon="food"
        )
        food_tab.add_widget(FoodTrackingScreen())
        
        # Exercise Tab
        exercise_tab = MDBottomNavigationItem(
            name="exercise",
            text="ব্যায়াম",  # Exercise
            icon="dumbbell"
        )
        exercise_tab.add_widget(ExerciseScreen())
        
        # Pantry Tab
        pantry_tab = MDBottomNavigationItem(
            name="pantry",
            text="প্যান্ট্রি",  # Pantry
            icon="food-variant"
        )
        pantry_tab.add_widget(PantryScreen())
        
        # Profile Tab
        profile_tab = MDBottomNavigationItem(
            name="profile",
            text="প্রোফাইল",  # Profile
            icon="account"
        )
        profile_tab.add_widget(ProfileScreen())
        
        # Add tabs to bottom navigation
        bottom_nav.add_widget(dashboard_tab)
        bottom_nav.add_widget(food_tab)
        bottom_nav.add_widget(exercise_tab)
        bottom_nav.add_widget(pantry_tab)
        bottom_nav.add_widget(profile_tab)
        
        main_screen.add_widget(bottom_nav)
        self.sm.add_widget(main_screen)
        
        return self.sm

class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.setup_ui()
        
    def setup_ui(self):
        layout = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(16))
        
        # Header
        header = MDLabel(
            text="আজকের সারাংশ",  # Today's Summary
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(header)
        
        # Stats Cards
        stats_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(120))
        
        # Calories Card
        calories_card = MDCard(
            size_hint=(0.5, 1),
            padding=dp(10)
        )
        calories_layout = MDBoxLayout(orientation='vertical')
        calories_layout.add_widget(MDLabel(text="ক্যালরি", halign="center", font_style="Caption"))
        calories_layout.add_widget(MDLabel(text="1,200/2,000", halign="center", font_style="H6"))
        calories_card.add_widget(calories_layout)
        
        # Water Card
        water_card = MDCard(
            size_hint=(0.5, 1),
            padding=dp(10)
        )
        water_layout = MDBoxLayout(orientation="vertical")
        water_layout.add_widget(MDLabel(text="পানি", halign="center", font_style="Caption"))
        water_layout.add_widget(MDLabel(text="6/8 গ্লাস", halign="center", font_style="H6"))
        water_card.add_widget(water_layout)
        
        stats_layout.add_widget(calories_card)
        stats_layout.add_widget(water_card)
        layout.add_widget(stats_layout)
        
        # Quick Actions
        actions_label = MDLabel(
            text="দ্রুত কাজ",  # Quick Actions
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(actions_label)
        
        actions_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(60))
        
        add_food_btn = MDRaisedButton(
            text="খাবার যোগ করুন",  # Add Food
            size_hint=(0.5, 1),
            on_release=self.add_food
        )
        
        add_exercise_btn = MDRaisedButton(
            text="ব্যায়াম যোগ করুন",  # Add Exercise
            size_hint=(0.5, 1),
            on_release=self.add_exercise
        )
        
        actions_layout.add_widget(add_food_btn)
        actions_layout.add_widget(add_exercise_btn)
        layout.add_widget(actions_layout)
        
        # Recent Activities
        recent_label = MDLabel(
            text="সাম্প্রতিক কার্যক্রম",  # Recent Activities
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(recent_label)
        
        # Scrollable recent activities
        scroll = MDScrollView()
        recent_list = MDList()
        
        # Add some dummy recent activities
        activities = [
            "ভাত + মাছ (৩০০ ক্যালরি)",
            "পুশ-আপ (১০ বার)",
            "পানি (১ গ্লাস)",
            "দুধ (১৫০ ক্যালরি)"
        ]
        
        for activity in activities:
            recent_list.add_widget(OneLineListItem(text=activity))
        
        scroll.add_widget(recent_list)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def add_food(self, instance):
        # Navigate to food tracking screen
        pass
    
    def add_exercise(self, instance):
        # Navigate to exercise screen
        pass

class FoodTrackingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.setup_ui()
        
    def setup_ui(self):
        layout = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(16))
        
        # Header
        header = MDLabel(
            text="খাবার ট্র্যাকিং",  # Food Tracking
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(header)
        
        # Search Bar
        search_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(60))
        search_field = MDTextField(
            hint_text="খাবার খুঁজুন...",  # Search food...
            size_hint=(0.7, 1)
        )
        search_btn = MDRaisedButton(
            text="খুঁজুন",  # Search
            size_hint=(0.3, 1)
        )
        search_layout.add_widget(search_field)
        search_layout.add_widget(search_btn)
        layout.add_widget(search_layout)
        
        # Quick Add Buttons
        quick_add_label = MDLabel(
            text="দ্রুত যোগ করুন",  # Quick Add
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(quick_add_label)
        
        # Pantry items grid
        pantry_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        
        # Common Bangladeshi foods
        common_foods = [
            ("ভাত", "Rice", "130"),
            ("রুটি", "Roti", "80"),
            ("মাছ", "Fish", "120"),
            ("মাংস", "Meat", "250"),
            ("ডাল", "Dal", "100"),
            ("সবজি", "Vegetables", "50")
        ]
        
        for i in range(0, len(common_foods), 2):
            row = MDBoxLayout(orientation='horizontal', spacing=dp(10))
            
            # First item
            food1 = common_foods[i]
            card1 = MDCard(size_hint=(0.5, 1), padding=dp(10))
            card1_layout = MDBoxLayout(orientation='vertical')
            card1_layout.add_widget(MDLabel(text=food1[0], halign="center"))
            card1_layout.add_widget(MDLabel(text=f"{food1[2]} ক্যালরি", halign="center", font_style="Caption"))
            card1.add_widget(card1_layout)
            row.add_widget(card1)
            
            # Second item (if exists)
            if i + 1 < len(common_foods):
                food2 = common_foods[i + 1]
                card2 = MDCard(size_hint=(0.5, 1), padding=dp(10))
                card2_layout = MDBoxLayout(orientation='vertical')
                card2_layout.add_widget(MDLabel(text=food2[0], halign="center"))
                card2_layout.add_widget(MDLabel(text=f"{food2[2]} ক্যালরি", halign="center", font_style="Caption"))
                card2.add_widget(card2_layout)
                row.add_widget(card2)
            
            pantry_layout.add_widget(row)
        
        layout.add_widget(pantry_layout)
        
        # Add custom food button
        add_custom_btn = MDRaisedButton(
            text="নতুন খাবার যোগ করুন",  # Add New Food
            on_release=self.show_add_food_dialog
        )
        layout.add_widget(add_custom_btn)
        
        self.add_widget(layout)
    
    def show_add_food_dialog(self, instance):
        # Show dialog to add custom food
        pass

class ExerciseScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.setup_ui()
        
    def setup_ui(self):
        layout = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(16))
        
        # Header
        header = MDLabel(
            text="ব্যায়াম",  # Exercise
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(header)
        
        # Level Filter Chips
        level_label = MDLabel(
            text="স্তর নির্বাচন করুন",  # Select Level
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(level_label)
        
        level_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        levels = ["শুরুর", "মাঝারি", "উন্নত"]  # Beginner, Intermediate, Advanced
        
        for level in levels:
            chip = MDChip(
                text=level,
                size_hint=(None, None),
                size=(dp(80), dp(40))
            )
            level_layout.add_widget(chip)
        
        layout.add_widget(level_layout)
        
        # Exercise Categories
        categories_label = MDLabel(
            text="ব্যায়ামের ধরন",  # Exercise Types
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(categories_label)
        
        # Exercise grid
        exercise_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        
        exercises = [
            ("পুশ-আপ", "Push-ups", "Beginner"),
            ("স্কোয়াট", "Squats", "Beginner"),
            ("প্লাঙ্ক", "Plank", "Intermediate"),
            ("বারপি", "Burpees", "Advanced"),
            ("লাঞ্জ", "Lunges", "Intermediate"),
            ("মাউন্টেন ক্লাইম্বার", "Mountain Climber", "Advanced")
        ]
        
        for i in range(0, len(exercises), 2):
            row = MDBoxLayout(orientation='horizontal', spacing=dp(10))
            
            # First exercise
            ex1 = exercises[i]
            card1 = MDCard(size_hint=(0.5, 1), padding=dp(10))
            card1_layout = MDBoxLayout(orientation='vertical')
            card1_layout.add_widget(MDLabel(text=ex1[0], halign="center"))
            card1_layout.add_widget(MDLabel(text=ex1[2], halign="center", font_style="Caption"))
            card1.add_widget(card1_layout)
            row.add_widget(card1)
            
            # Second exercise (if exists)
            if i + 1 < len(exercises):
                ex2 = exercises[i + 1]
                card2 = MDCard(size_hint=(0.5, 1), padding=dp(10))
                card2_layout = MDBoxLayout(orientation='vertical')
                card2_layout.add_widget(MDLabel(text=ex2[0], halign="center"))
                card2_layout.add_widget(MDLabel(text=ex2[2], halign="center", font_style="Caption"))
                card2.add_widget(card2_layout)
                row.add_widget(card2)
            
            exercise_layout.add_widget(row)
        
        layout.add_widget(exercise_layout)
        
        # Create routine button
        create_routine_btn = MDRaisedButton(
            text="রুটিন তৈরি করুন",  # Create Routine
            on_release=self.create_routine
        )
        layout.add_widget(create_routine_btn)
        
        self.add_widget(layout)
    
    def create_routine(self, instance):
        # Show routine creation dialog
        pass

class PantryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.setup_ui()
        
    def setup_ui(self):
        layout = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(16))
        
        # Header
        header = MDLabel(
            text="আমার প্যান্ট্রি",  # My Pantry
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(header)
        
        # Add to pantry button
        add_btn = MDRaisedButton(
            text="প্যান্ট্রিতে যোগ করুন",  # Add to Pantry
            on_release=self.show_add_pantry_dialog
        )
        layout.add_widget(add_btn)
        
        # Pantry items
        pantry_label = MDLabel(
            text="আপনার খাবার",  # Your Foods
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(pantry_label)
        
        # Scrollable pantry list
        scroll = MDScrollView()
        pantry_list = MDList()
        
        # Dummy pantry items
        pantry_items = [
            "ভাত (১ কাপ) - ১৩০ ক্যালরি",
            "মাছ (১০০ গ্রাম) - ১২০ ক্যালরি",
            "ডিম (১টি) - ৭০ ক্যালরি",
            "দুধ (১ গ্লাস) - ১৫০ ক্যালরি",
            "কলা (১টি) - ১০৫ ক্যালরি",
            "আপেল (১টি) - ৯৫ ক্যালরি"
        ]
        
        for item in pantry_items:
            pantry_list.add_widget(OneLineListItem(text=item))
        
        scroll.add_widget(pantry_list)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def show_add_pantry_dialog(self, instance):
        # Show dialog to add item to pantry
        pass

class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.setup_ui()
        
    def setup_ui(self):
        layout = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(16))
        
        # Header
        header = MDLabel(
            text="প্রোফাইল",  # Profile
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(header)
        
        # Profile info
        profile_card = MDCard(padding=dp(16))
        profile_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        
        profile_layout.add_widget(MDLabel(text="নাম: আহমেদ", font_style="H6"))
        profile_layout.add_widget(MDLabel(text="বয়স: ২৫ বছর", font_style="Body1"))
        profile_layout.add_widget(MDLabel(text="ওজন: ৭০ কেজি", font_style="Body1"))
        profile_layout.add_widget(MDLabel(text="উচ্চতা: ৫'৮\"", font_style="Body1"))
        profile_layout.add_widget(MDLabel(text="লক্ষ্য: ওজন কমানো", font_style="Body1"))
        
        profile_card.add_widget(profile_layout)
        layout.add_widget(profile_card)
        
        # Settings buttons
        settings_label = MDLabel(
            text="সেটিংস",  # Settings
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(settings_label)
        
        # Settings options
        settings_list = MDList()
        settings_items = [
            "প্রোফাইল সম্পাদনা করুন",  # Edit Profile
            "লক্ষ্য পরিবর্তন করুন",  # Change Goal
            "ভাষা পরিবর্তন করুন",  # Change Language
            "বিজ্ঞপ্তি সেটিংস",  # Notification Settings
            "ডেটা রপ্তানি করুন",  # Export Data
            "সাহায্য",  # Help
            "লগআউট"  # Logout
        ]
        
        for item in settings_items:
            settings_list.add_widget(OneLineListItem(text=item))
        
        layout.add_widget(settings_list)
        
        self.add_widget(layout)

# Database class is now imported from database.py

if __name__ == '__main__':
    BangladeshiFitnessApp().run() 