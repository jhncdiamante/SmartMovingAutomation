@echo off
cd /d "D:\Freelancing Documents\SmartMoving\SmartMovingBot"
call venv\Scripts\activate.bat
python -m src.sales_dashboard_task
deactivate
pause

