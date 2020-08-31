from django.contrib.auth import authenticate


class Server:
    def __init__(self):
        self.isLogged = False
        self.user = None
        self.menu()

    def login(self, user_login, password):
        user = authenticate(username=user_login, password=password)
        if user is not None:
            self.isLogged = True
            self.user = user
            print(user)
        else:
            print("Invialid credentials")

        self.menu()

    def menu(self):
        print("*** MENU ***\n")
        if self.isLogged:
            print("1. Logout\n")
            print("2. End\n")

        else:
            print("1. Login")
            print("2. End")
            choise = input("Wybor: ")
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