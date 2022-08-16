# RestaurantApp

Dockerized ReactJs with Django and Postgres

Init step by step:

1. Clone repository (git clone https://github.com/Snowflake97/RestaurantApp.git)
2. Under ./frontend/ directory install npm (npm i)
3. After npm install './fronted/node_modules/' directory should be visible - frontend docker container will be using
   this directory
4. Build and run containers (docker-compose up -d --build):
    - database
    - backend
    - frontend
5. Database migration (docker-compose exec backend python manage.py migrate)
6. Create superuser (docker-compose exec backend python manage.py createsuperuser)
7. Enter username, mail and password to create superuser
8. For backend admin login open http://localhost:8000/admin and log in
9. For backend rest api open http://localhost:8000/api/
10. For frontend open http://localhost:3000/ - page should fetch users from backend rest api and show it on screen
    (please double-check container console if server is already running)
