#!/bin/bash
echo "Starting MOOC Catalog with Docker..."

# Build and start containers
docker-compose up --build -d

echo ""
echo "Waiting for services to start..."
sleep 10

# Create superuser prompt
echo ""
read -p "Would you like to create a superuser? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose exec web python manage.py createsuperuser
fi

echo ""
echo "MOOC Catalog is running!"
echo "Access the application at http://localhost:8000"
echo "Admin panel at http://localhost:8000/admin"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
