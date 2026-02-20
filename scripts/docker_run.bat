@echo off
echo Starting MOOC Catalog with Docker...

:: Build and start containers
docker-compose up --build -d

echo.
echo Waiting for services to start...
timeout /t 10 /nobreak

:: Create superuser prompt
echo.
echo Would you like to create a superuser? (y/n)
set /p create_super=
if /i "%create_super%"=="y" (
    docker-compose exec web python manage.py createsuperuser
)

echo.
echo MOOC Catalog is running!
echo Access the application at http://localhost:8000
echo Admin panel at http://localhost:8000/admin
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down
