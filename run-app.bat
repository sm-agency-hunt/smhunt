@echo off
echo Starting SMHunt Application...
echo.
echo Access the API at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo Login with: admin@smhunt.online / admin123
echo.
python -m uvicorn simple_app:app --host 0.0.0.0 --port 8000 --reload