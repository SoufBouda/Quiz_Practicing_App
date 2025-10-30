@echo off
echo Starting the quiz application...
start "Quiz App" python app.py
start "Admin App" python admin_app.py
start http://127.0.0.1:5000
echo Application is running.
pause
