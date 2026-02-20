#!/bin/bash
echo "Setting up MOOC Catalog locally..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser prompt
echo ""
read -p "Would you like to create a superuser? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Run development server
echo ""
echo "Starting development server..."
echo "Access the application at http://localhost:8000"
echo "Admin panel at http://localhost:8000/admin"
python manage.py runserver
