Write-Host "Starting SMHunt Application..." -ForegroundColor Green
Write-Host ""
Write-Host "Access the API at: http://localhost:8000" -ForegroundColor Yellow
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "Login with: admin@smhunt.online / admin123" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn simple_app:app --host 0.0.0.0 --port 8000 --reload