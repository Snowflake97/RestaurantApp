from django.contrib.auth import authenticate
from restaurantApp.models import *
from functions import *


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
            print("\nBledne dane logowania")

        self.menu()

    def menu(self):
        print("*** MENU ***\n")
        if self.isLogged:
            print("1. Skladniki")
            print("2. Produkty")
            print("3. Zamowienia")
            print("4. Magazyn")
            print("5. Pracownicy")
            print("6. Rezerwacje")
            print("7. Raporty")

            print("8. Wyloguj sie\n")
            choise = input("\nWybor: ")

            if choise == "1":
                self.manage_ingredients()
            elif choise == "2":
                self.manage_products()
            elif choise == "3":
                self.manage_orders()
            elif choise == "4":
                self.manage_storages()
            elif choise == "5":
                self.manage_employees()
            elif choise == "6":
                self.manage_reservation()
            elif choise == "7":
                self.raports()
            elif choise == "8":
                self.__init__()
            if choise != "8":
                self.menu()
        else:
            print("1. Zaloguj sie")
            print("2. Koniec")
            choise = input("\nWybor: ")
            if choise == "1":
                log = input("Login: ")
                password = input("Haslo: ")
                self.login(log, password)

            elif choise == "2":
                pass

    def manage_ingredients(self):
        print("1. Dodaj")
        print("2. Usun")
        print("0. Wroc")
        choice = int(input("--> Wybor:"))
        if choice == 1:
            self.create_ingredient()
        elif choice == 2:
            self.delete_object(Ingredient)
        elif choice == 0:
            self.menu()

    def manage_products(self):
        print("1. Dodaj")
        print("2. Usun")
        print("0. Wroc")
        choice = int(input("--> Wybor:"))
        if choice == 1:
            self.create_product()
        elif choice == 2:
            self.delete_object(Product)
        elif choice == 0:
            self.menu()

    def manage_orders(self):
        print("1. Dodaj")
        print("2. Usun")
        print("3. Edytuj aktywne zamowienie")
        print("0. Wroc")
        choice = int(input("--> Wybor:"))
        if choice == 1:
            self.create_order()
        elif choice == 2:
            self.delete_object(Order)
        elif choice == 3:
            orders = self.active_orders()
            for position, order in enumerate(orders):
                print(f"{position+1}. {order}")
                choise = int(input("--> Wybor:"))
                self.manage_order(orders[position-1])
        elif choice == 0:
            self.menu()

    def manage_storages(self):
        storage = self.pick_object(Storage)
        print("1. Dodaj")
        print("2. Edytuj")
        print("0. Wroc")
        choice = int(input("--> Wybor:"))
        if choice == 1:
            value = int(input("--> Ilosc do dodania:"))
            storage.add_quantity(value)
        elif choice == 2:
            value = int(input("--> Ilosc nadpisywana:"))
            storage.edit_quantity(value)
        elif choice == 0:
            self.menu()

    def manage_employees(self):
        print("1. Dodaj")
        print("2. Usun")
        print("0. Wroc")
        choice = int(input("--> Wybor:"))
        if choice == 1:
            self.create_employee()
        elif choice == 2:
            self.delete_object(Employee)
        elif choice == 0:
            self.menu()

    def manage_reservation(self):
        print("1. Dodaj")
        print("2. Usun")
        print("0. Wroc")
        choice = int(input("--> Wybor:"))
        if choice == 1:
            self.create_reservation()
        elif choice == 2:
            self.delete_object(Reservation)
        elif choice == 0:
            self.menu()

    def logout(self):
        if self.isLogged:
            self.isLogged = False
            self.user = None
        self.menu()

    def pick_object(self, objects):
        objects = objects.objects.all()
        for position, object in enumerate(objects):
            print(f"{position + 1}. {object}")

        choise = int(input("--> Wybór:"))
        return objects[choise - 1]

    def delete_object(self, object):
        object = self.pick_object(object)
        object.delete()

    def new_order(self):
        order = Order.objects.create(employee=self.current_employee)
        order.save()
        return order

    def new_ingredient(self, name, quantity_type, ingredient_type):
        ingredient = Ingredient.objects.create(name=name, ingredient_type=ingredient_type, quantity_type=quantity_type)
        ingredient.save()
        return ingredient

    def new_product(self, product_name, product_price, product_type, ingredients_quantity_list):
        product = Product.objects.create(name=product_name, price=product_price, product_type=product_type)
        product.save()
        for ingredient, quantity in ingredients_quantity_list:
            product_ingredient = ProductIngredient.objects.create(product=product, ingredient=ingredient,
                                                                  quantity_usage=quantity)
            product_ingredient.save()

    def new_address(self, street_name, street_number, house_number, zip_code, city):
        address = Address.objects.create(street_name=street_name, street_number=street_number,
                                         house_number=house_number, zip_code=zip_code, city=city)
        address.save()
        return address

    def new_restaurant(self, address):
        restaurant = Restaurant.objects.create(address=address)
        restaurant.save()
        return restaurant

    def new_person(self, first_name, last_name, address, phone_number):
        person = Person.objects.create(first_name=first_name, last_name=last_name, address=address,
                                       phone_number=phone_number)
        person.save()
        return person

    def new_user(self, user_name, password):
        user = User.objects.create(username=user_name)
        user.set_password(password)
        user.save()
        return user

    def new_employee(self, user, person, position, restaurant):
        employee = Employee.objects.create(person=person, user=user, restaurant=restaurant, position=position)
        employee.save()
        return employee

    def new_table(self, seats, table_number, restaurant):
        table = Table.objects.create(table_number=table_number, restaurant=restaurant, chairs_quantity=seats)
        table.save()
        return table

    def new_restaurant(self, address):
        restaurant = Restaurant.objects.create(address=address)
        restaurant.save()
        return restaurant

    def edit_product(self, product, product_name, product_price, product_type, ingredients_quantity_list):
        product.name = product_name
        product.price = product_price
        product.product_type = product_type
        ProductIngredient.objects.filter(product=product).delete()
        for ingredient, quantity in ingredients_quantity_list:
            product_ingredient = ProductIngredient.objects.create(product=product, ingredient=ingredient,
                                                                  quantity_usage=quantity)
            product_ingredient.save()
        product.save()


    def delete_object(self, object):
        object = self.pick_object(object)
        object.delete()

    def get_quantity_type(self):
        print("--> Wybór typu ilości:")
        print("1. Sztuki")
        print("2. Gramy")
        choise = input("Wybor: ")
        if choise == "1":
            quantity_type = "SZT"
        elif choise == "2":
            quantity_type = "GR"
        else:
            quantity_type = None
        return quantity_type

    def get_ingredient_type(self):
        print("--> Wybór typu składnika:")
        print("1. Ser")
        print("2. Mieso")
        print("3. Warzywo")
        print("4. Napój")

        choise = input("Wybor: ")
        if choise == "1":
            ingredient_type = "S"
        elif choise == "2":
            ingredient_type = "M"
        elif choise == "3":
            ingredient_type = "W"
        elif choise == "4":
            ingredient_type = "N"
        else:
            ingredient_type = "NOT_DEF"
        return ingredient_type

    def get_product_type(self):
        print("--> Wybór typu produktu:")
        print("1. Posilek")
        print("2. Napoj")

        choise = input("Wybor: ")
        if choise == "1":
            product_type = "P"
        elif choise == "2":
            product_type = "N"

        return product_type

    def ingredients_list(self):
        ingredients = []
        all_ingredients = Ingredient.objects.all()
        while True:
            for position, ingredient in enumerate(all_ingredients):
                print(f"{position + 1}. {ingredient.name}")
            choice = int(input("Wybor: "))
            quantity = int(input("Ilość składnika: "))
            ingredients.append((all_ingredients[choice - 1], quantity))
            choice = input("Dodac nastepny? (y/n): ")
            if choice != "y":
                return ingredients

    def create_product(self):
        name = input("--> Nazwa produktu: ")
        price = float(input("--> Cena: "))
        product_type = self.get_product_type()
        ingredients_list = self.ingredients_list()
        self.new_product(name, price, product_type, ingredients_list)

    def create_ingredient(self):
        name = input("--> Nazwa skladnika: ")
        ingredient_type = self.get_ingredient_type()
        quantity_type = self.get_quantity_type()
        self.new_ingredient(name=name, quantity_type=quantity_type, ingredient_type=ingredient_type)

    def create_user(self):
        username = input("--> Nazwa uzytkownika: ")
        if User.objects.filter(username=username).exists():
            print("Wybrana nazwa jest zajeta\n")
            self.create_user()
        else:
            password = input("--> Haslo uzytkownika: ")
            return self.new_user(username, password)

    def create_person(self):
        first_name = input("--> Imie uzytkownika: ")
        last_name = input("--> Nazwisko uzytkownika: ")
        phone_number = input("--> Telefon: ")
        address = self.create_address()
        return self.new_person(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address)

    def create_employee(self):
        user = self.create_user()
        person = self.create_person()
        restaurant = self.pick_object(Restaurant)
        self.new_employee(user=user, person=person, restaurant=restaurant, position="W")

    def create_address(self):
        street_name = input("--> Nazwa ulicy: ")
        street_number = input("--> Numer ulicy: ")
        house_number = input("--> Numer domu(opcjonalne): ")
        zip_code = input("--> Kod pocztowy: ")
        city = input("--> Miasto: ")

        return self.new_address(street_name=street_name, street_number=street_number,
                                house_number=house_number, zip_code=zip_code, city=city)

    def create_resturant(self):
        address = self.create_address()
        return self.new_restaurant(address=address)

    def active_orders(self):
        orders = Order.objects.filter(employee=self.current_employee, status="A")
        return orders

    def create_order(self):
        order = self.new_order()
        self.manage_order(order)

    def manage_order(self, order):
        print("\n1. Dodaj produkt")
        print("2. Wyswietl produkty")
        print("3. Usun produkt")
        print("4. Zamknij zamowienie")
        choise = int(input("--> Wybór:"))
        if choise == 1:
            product = self.pick_object(Product)
            quantity = int(input("--> Ilosc sztuk:"))
            order.add_product(product, quantity)
        elif choise == 2:
            products = order.get_products()
            print("\nLista produktow: ")
            for product in products:
                print(f"- {product.name} x{order.get_product_quantity(product)}")
        elif choise == 3:
            products = order.get_products()
            if products:
                print("\nLista produktow: ")
                for position, product in enumerate(products):
                    print(f"{position + 1} {product.name} x{order.get_product_quantity(product)}")
                delete_position = int(input("--> Wybór:"))
                product = products[delete_position - 1]
                order.remove_product(product)
            else:
                print("Brak produktow")

        elif choise == 4:
            print("\nRodzaj platnosci:")
            print("1. Gotowka")
            print("2. Karta")
            choise = int(input("--> Wybor:"))
            if choise == 1:
                order.close_order(payment_method="G")
            elif choise == 2:
                order.close_order(payment_method="K")

        if order.status == "A":
            self.manage_order(order)
        else:
            self.menu()

    def create_reservation(self):
        restuarant = self.pick_object(Restaurant)
        print("--> Data:")
        date = create_date()
        print("--> Godzina rozpoczecia:")
        start_hour = create_hour()
        print("--> Godzina zakonczenia:")
        end_hour = create_hour()
        free_tables = restuarant.free_tables(date=date, reservation_start=start_hour, reservation_end=end_hour)
        if free_tables:
            for position, table in enumerate(free_tables):
                print(f"{position + 1}. {table.table_number}, ilosc miejsc: {table.chairs_quantity}")
            choise = int(input("--> Wybor: "))

            name = input("--> Nazwisko: ")
            phone = input("--> Telefon kontaktowy: ")
            free_tables[choise - 1].make_reservation(client_name=name, client_phone=phone, date=date,
                                                     reservation_start=start_hour, reservation_end=end_hour)
            print("Zarezerwowano")
        else:
            print("Brak wolnych stolikow")
        self.menu()

    def raports(self):
        restuarant = self.pick_object(Restaurant)
        print("--> Data rozpoczecia:")
        start_date = create_date()
        print("--> Data zakonczenia:")
        end_date = create_date()
        income = restuarant.get_income_from_time_period(start_date, end_date)
        products = restuarant.get_products_from_time_period(start_date, end_date)
        ingredients = restuarant.get_ingredients_usage_from_time_period(start_date, end_date)
        print(f"Utarg: {income}")

        print("Sprzedane produkty:")
        for product in products:
            print(f"- {product} x{products[product]}")

        print("Zuzyte skladniki:")
        for ingredient in ingredients:
            print(f"- {ingredient} x{ingredients[ingredient]}")
