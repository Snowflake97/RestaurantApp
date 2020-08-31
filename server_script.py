import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Inzynierka.settings'

import django

django.setup()

from django.contrib.auth import authenticate
from Server import Server

server = Server()

