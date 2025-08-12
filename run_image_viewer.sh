#!/bin/bash

echo "Starting PyQt6 Image Viewer..."
echo ""
echo "If you see any errors, make sure PyQt6 is installed:"
echo "pip install PyQt6"
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    python3 image_viewer.py
elif command -v python &> /dev/null; then
    python image_viewer.py
else
    echo "Error: Python not found. Please install Python 3.7 or higher."
    exit 1
fi
