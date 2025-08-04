#!/usr/bin/env python3
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the app
from main import BangladeshiFitnessApp

if __name__ == '__main__':
    BangladeshiFitnessApp().run()
