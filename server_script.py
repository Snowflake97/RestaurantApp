import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Inzynierka.settings'

import django

django.setup()

from django.contrib.auth import authenticate
from Server import *
from restaurantApp.models import *

server = Server()

# server.current_employee = Employee.objects.get(user__username="adi")

# server.raports()