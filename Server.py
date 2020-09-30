from django.contrib.auth import authenticate
from restaurantApp.models import *


class Server:
    def __init__(self):
        self.isLogged = False
        self.user = None
        self.current_employee = None
        self.menu()

    def login(self, user_login, password):
        user = authenticate(username=user_login, password=password)
        if user is not None:
            self.isLogged = True
            self.user = user
            self.current_employee = Employee.objects.get(user__username=user_login)
            print(f"\nWitaj, {self.current_employee.person}")
        else:
            print("\nInvialid credentials")

        self.menu()

    def menu(self):
        print("*** MENU ***\n")
        if self.isLogged:
            print("1. Logout\n")
            print("2. Koniec\n")

        else:
            print("1. Login")
            print("2. Koniec")
            choise = input("\nWybor: ")
            if choise == "1":
                log = input("Login: ")
                password = input("Password: ")
                self.login(log, password)
            elif choise == "2":
                pass

    def logout(self):
        if self.isLogged:
            self.isLogged = False
            self.user = None
        self.menu()