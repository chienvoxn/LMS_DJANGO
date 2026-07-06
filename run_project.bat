@echo off

call ./init_project.bat

start "Backend" cmd /k "cd ./lms_api && ..\venv\Scripts\python.exe manage.py runserver"

start "Frontend" cmd /k "cd ./lms_frontend && npm run dev"