@echo off
echo Setting up MOOC Catalog locally...

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Run migrations
echo Running migrations...
python manage.py migrate

:: Create superuser prompt
echo.
echo Would you like to create a superuser? (y/n)
set /p create_super=
if /i "%create_super%"=="y" (
    python manage.py createsuperuser
)

:: Run development server
echo.
echo Starting development server...
echo Access the application at http://localhost:8000
echo Admin panel at http://localhost:8000/admin
python manage.py runserver
