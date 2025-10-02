@echo off
cd /d "PATH_TO_YOUR_PROJECT"
call venv\Scripts\activate.bat
python -m src.sales_dashboard_task
deactivate
pause

