#!/usr/bin/env python3
"""
Test script to verify PyQt6 installation.

Run this script to check if PyQt6 is properly installed:
    python test_installation.py
"""

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QPixmap
    print("✓ PyQt6 successfully imported!")
    print("✓ All required modules are available")
    print("\nYou can now run the image viewer with:")
    print("    python image_viewer.py")
    
except ImportError as e:
    print("✗ Error importing PyQt6:")
    print(f"  {e}")
    print("\nTo install PyQt6, run:")
    print("    pip install PyQt6")
    print("\nOr install from requirements.txt:")
    print("    pip install -r requirements.txt")

except Exception as e:
    print(f"✗ Unexpected error: {e}")
