Useful information for preparing initial project with docker, django, reactjs and postgres:
1.Docker:
    1.1 docker-compose.yml determines 3 services/containers which would be build:
        1.1.1 database:
            - define default postgres image 
            - define env_file - file which contains ENV variables.
            - map volume (./database/db:/var/lib/postgresql/data) -> local_directory:container_directory 
                #NOTE since volumes are connected after first docker build database directory should be visible 
                      under local files.
        1.1.2 backend:
            - define build - point directory which contains Dockerfile for this container build
            - define command - command which should be executed after container build
            - define env_file - file which contains ENV variables.
            - map volume (./backend:/backend) -> local_directory:container_directory 
                #NOTE since volumes are connected changing local files should automatically trigger django hot-reload
            - define ports forwarding - 8000:8000 -> local_port:container_port
            - define dependencies - configure when service depends on other service/services
        1.1.3 frontend:
            - define build - point directory which contains Dockerfile for this container build
            - define command - command which should be executed after container build
            - map volume (./frontend:/frontend) -> local_directory:container_directory 
                #NOTE since volumes are connected changing local files should automatically trigger django hot-reload
            - define ports forwarding - 3000:3000 -> local_port:container_port
            - define dependencies - configure when service depends on other service/services
    1.2 ./backend/Dockerfile - instructions where and how create container for backend:
        - define default docker image (FROM python:3.10-alpine)
        - define workspace container_directory (WORKDIR /backend)
            #NOTE defined workspace must match with volume mapped in docker-compose.yml
        - define dependencies which should be installed inside container 
        - copy requirements.txt to container and install dependencies
        - copy rest of project to container
    1.3 ./frontend/Dockerfile - instructions where and how create container for frontend:
        - define default docker image (FROM node:16.13.1-alpine)
        - define workspace container_directory (WORKDIR /frontend)
            #NOTE defined workspace must match with volume mapped in docker-compose.yml
        - copy package.json to container
        - run npm install to install all modules defined in package.json.
        - copy src and public directories to container 
        - expose port 3000
2. Backend:
    2.1 backend - main project app:
        2.1.1 ./backend/backend/settings.py
            - for development purpose ALLOWED_HOSTS are set to '*' which allows every host to connect
            - added 'rest-framework' and 'api' to INSTALLED_APPS
            - configure postgresql database engine and read database parameter from ENV variables
            - configure REST_FRAMEWORK 
            - configure CORS_ORIGIN_WHITELIST - add and allow frontend url
        2.1.2 ./backend/backend/urls.py:
            - include urls from api app
    2.2 api - restfull api app
        2.2.1 ./backend/api/serializers.py
            - create serializers by creating class which inherit from rest_framework 
              serializers.HyperlinkedModelSerializer
            - using metaclass define 'model' and 'fields' parameters ('model' is database model name and 'fields' 
              is list of database model attributes names which api should pass further)
        2.2.2 ./backend/api/views.py
            - create "Class-based views" (https://docs.djangoproject.com/en/4.0/topics/class-based-views/) class which 
              inherit form viewsets.ModelViewSet from rest_framework and just specify 'queryset' and 'serializer_class'
              ('queryset' should contain objects from database and 'serializer_class' is class which tells which model 
               and what attributes should be translated to json format)
        2.2.3 ./backend/api/urls.py
            - create and configure routers.DefaultRouter() instance from rest_framework
            - register to router endpoints names with views which should be invoked
            - to urlpatterns append new patch with endpoint for api interface and include created urls 
              in router instance
3. Frontend:
   3.1 ./frontend/package.json:
        3.1.1 add and configure proxy:
            - add line: "proxy" : "http://backend:8000"
                #NOTE while running in docker container proxy should contain service name instead of localhost