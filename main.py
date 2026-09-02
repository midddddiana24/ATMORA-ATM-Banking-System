#!/usr/bin/env python3
"""
ATMORA — Modern ATM Banking System
=====================================

Entry Point

Run this file to launch the application:
    python main.py

Academic Context:
    Course:     CIT 240 – Open Source Programming
    Activity:   Midterm Laboratory Activity No. 5
    School:     West Visayas State University – Janiuay Campus
    Year:       1st Semester SY 2026–2027

Developer:
    Roberto Mediana Jr
    GitHub: https://github.com/midddddiana24

DEMO ACCOUNT (for classroom use only — not real banking data):
    Account Number: 10010001
    PIN:            1234

⚠ DISCLAIMER:
    This is an educational simulation. It is NOT a real banking system.
    No real financial data is used or processed.
"""

import sys
import os

# Add the src directory to Python path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def main():
    """
    Application entry point.
    
    Imports and launches the ATMORAApp.
    Handles startup errors gracefully.
    """
    try:
        from app import ATMORAApp
        app = ATMORAApp()
        app.run()

    except ImportError as e:
        print(f"\n⚠  Missing dependency: {e}")
        print("Please install required packages:")
        print("    pip install customtkinter pillow\n")
        sys.exit(1)

    except Exception as e:
        print(f"\n⚠  Startup error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
