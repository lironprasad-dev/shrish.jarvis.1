@echo off
title JARVIS-LOQ Server
color 0A
echo.
echo  ========================================
echo    JARVIS-LOQ Backend Server
echo    Lenovo LOQ - RTX 5050 - Intel Core i7
echo  ========================================
echo.
echo  Installing packages if needed...
pip install flask flask-cors --quiet
echo.
echo  Starting server on http://localhost:5050
echo  Keep this window OPEN while using JARVIS
echo  Press Ctrl+C to stop
echo.
python jarvis_server.py
pause
