#!/bin/bash
echo "Starting the quiz application..."
python app.py --no-reload > app.log 2>&1 &
python admin_app.py > admin_app.log 2>&1 &
xdg-open http://127.0.0.1:5000
echo "Application is running."
