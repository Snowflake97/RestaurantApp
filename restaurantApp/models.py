from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
import datetime


# Create your models here.
# class IngredientType(models.Model):
#     INGREDIENT_TYPES = (
#         ('ND', 'NOT DEFINED'),
#         ('S', 'Ser'),
#         ('M', 'Mięso'),
#         ('W', 'Warzywo'),
#         ('N', 'Napój'),
#     )
#     ingredient_type = models.CharField(max_length=3, choices=INGREDIENT_TYPES, default='ND')
#
#     def __str__(self):
#         return self.ingredient_type

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    QUANTITY_TYPES = (
        ('GR', 'Gramy'),
        ('SZT', 'Sztuki')
    )
    quantity_type = models.CharField(max_length=3, choices=QUANTITY_TYPES, default='GR')
    INGREDIENT_TYPES = (
        ('ND', 'NOT DEFINED'),
        ('S', 'Ser'),
        ('M', 'Mięso'),
        ('W', 'Warzywo'),
        ('N', 'Napój'),
    )
    ingredient_type = models.CharField(max_length=3, choices=INGREDIENT_TYPES, default='ND')

    def __str__(self):
        return f"{self.name} ({self.quantity_type})"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        for restaurant in Restaurant.objects.all():
            storage = Storage.objects.create(ingredient_id=self.id, restaurant=restaurant, quantity=0)
            storage.save()


class Address(models.Model):
    street_name = models.CharField(max_length=100)
    street_number = models.IntegerField()
    house_number = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        if self.house_number:
            return f"{self.street_name} {self.street_number}/{self.house_number} {self.zip_code} {self.city}"
        else:
            return f"{self.street_name} {self.street_number} {self.zip_code} {self.city}"


class Restaurant(models.Model):
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Restaurant, self).save()
        for ingredient in Ingredient.objects.all():
            storage = Storage.objects.create(restaurant_id=self.id, ingredient=ingredient, quantity=0)
            storage.save()

    def __str__(self):
        return f"Oddział {self.address.city}(ul. {self.address.street_name})"

    def get_orders_from_time_period(self, date_start, date_end):
        orders_from_restuarant = []
        orders = Order.objects.filter(date__range=[date_start, date_end])
        for order in orders:
            if order.employee.restaurant.id == self.id:
                orders_from_restuarant.append(order)
        return orders_from_restuarant

    def get_products_from_time_period(self, date_start, date_end):
        products_dictonary = {}
        orders = self.get_orders_from_time_period(date_start, date_end)
        for order in orders:
            for product_order in ProductOrder.objects.filter(order=order):
                product = product_order.product
                quantity = product_order.quantity
                if product:
                    if products_dictonary.get(product):
                        products_dictonary[product] += quantity
                    else:
                        products_dictonary = {**products_dictonary, **{product:quantity}}
        return products_dictonary

    def get_ingredients_usage_from_time_period(self, date_start, date_end):
        ingredients_dictonary = {}
        orders = self.get_orders_from_time_period(date_start, date_end)
        for order in orders:
            order_ingredients = order.get_ingredients_usage()
            for order_ing in order_ingredients:
                if ingredients_dictonary.get(order_ing):
                    ingredients_dictonary[order_ing] += order_ingredients[order_ing]
                else:
                    ingredients_dictonary = {**ingredients_dictonary, **{order_ing: order_ingredients[order_ing]}}

        return ingredients_dictonary

    def get_income_from_time_period(self, date_start, date_end):
        orders = self.get_orders_from_time_period(date_start, date_end)
        total_value = 0
        for order in orders:
            total_value += order.total_price

        return round(total_value,2)


class Storage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.restaurant} - {self.ingredient.name} ({self.quantity} {self.ingredient.quantity_type})"

    def save(self, *args, **kwargs):
        self.quantity = round(self.quantity, 2)
        super().save(*args, **kwargs)

    def add_quantity(self, quantity):
        self.quantity += quantity
        self.save()

    def edit_quantity(self, quantity):
        self.quantity = quantity
        self.save()



class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

    PRODUCT_TYPES = (
        ('N', 'Napój'),
        ('P', 'Posiłek'),
        ('D', 'Dodatek')
    )
    product_type = models.CharField(max_length=3, choices=PRODUCT_TYPES, default='P')

    def __str__(self):
        return f"{self.name} ({self.price})"

    def get_ingredients_with_quantity(self):
        ingredients = []
        products_ingredients = ProductIngredient.objects.filter(product_id=self.id)
        for product_ingredient in products_ingredients:
            ingredients.append((product_ingredient.ingredient, product_ingredient.quantity_usage))

        return ingredients

    def get_ingredients(self):
        ingredients = []
        products_ingredients = ProductIngredient.objects.filter(product_id=self.id)
        for product_ingredient in products_ingredients:
            ingredients.append((product_ingredient.ingredient))

        return ingredients

    def is_ingredient_type_in_product(self, ingredient_type):
        ingredients = self.get_ingredients()
        for ingredient in ingredients:
            if ingredient.ingredient_type == ingredient_type:
                return True
        return False


class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_usage = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.ingredient.name} ({self.quantity_usage} {self.ingredient.quantity_type})"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

        for restaurant in Restaurant.objects.all():
            if Storage.objects.filter(ingredient=self.ingredient, restaurant=restaurant).count() == 0:
                storage = Storage.objects.create(ingredient=self.ingredient, quantity=0, restaurant=restaurant)
                storage.save()


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Numer telefonu powinien zawierać się w formacie +48999999999")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Employee(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    POSITIONS = (
        ('M', 'Manager'),
        ('W', 'Pracownik')
    )
    position = models.CharField(max_length=1, choices=POSITIONS)

    def __str__(self):
        return f"{self.person} ({self.get_position_display()})"


class Order(models.Model):
    # restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default=None)
    total_price = models.FloatField(default=0)

    STATUS_TYPES = (
        ('A', 'Aktywne'),
        ('Z', 'Zamknięte')
    )
    status = models.CharField(max_length=1, choices=STATUS_TYPES, default='A')

    PAYMENT_TYPES = (
        ('G', 'Gotówka'),
        ('K', 'Karta')
    )
    payment = models.CharField(max_length=1, choices=PAYMENT_TYPES, null=True, blank=True)

    def get_products(self):
        products = []
        for product_order in ProductOrder.objects.filter(order_id=self.id):
            products.append(product_order.product)

        return products

    def get_price(self):
        self.recalculate_total_price()
        return self.total_price

    def recalculate_total_price(self):
        total_price = 0
        for product_order in ProductOrder.objects.filter(order_id=self.id):
            total_price = total_price + product_order.product.price * product_order.quantity
        self.total_price = total_price
        super().save()

    def add_product(self, product, quantity):
        if ProductOrder.objects.filter(product=product, order_id=self.id).count() == 0:
            product_order = ProductOrder.objects.create(product=product, quantity=quantity, order_id=self.id)
        else:
            product_order = ProductOrder.objects.get(product=product, order_id=self.id)
            product_order.quantity += quantity
        self.recalculate_total_price()
        product_order.save()

    def get_product_quantity(self, product):
        quantity = ProductOrder.objects.get(order_id=self.id, product=product).quantity
        return quantity

    def __str__(self):
        return f"Zamowienie: {self.id}"

    def close_order(self, payment_method):
        if self.status == 'A':
            self.status = 'Z'
            self.payment = payment_method
            restaurant = Restaurant.objects.get(employee=self.employee)
            products_order = ProductOrder.objects.all().filter(order_id=self.id)
            for product in products_order:
                product_order_quantity = product.quantity
                product_ingredients = ProductIngredient.objects.filter(product=product.product)
                for product_ingredient in product_ingredients:
                    ingredient = product_ingredient.ingredient
                    quantity = product_ingredient.quantity_usage
                    storage = Storage.objects.get(ingredient=ingredient, restaurant=restaurant)
                    storage.quantity -= quantity * product_order_quantity
                    if storage.quantity < 0:
                        storage.quantity = 0
                    storage.save()
            super().save()

    def get_ingredients_usage(self):
        ingredients_dictonary = {}
        products = self.get_products()
        for product in products:
            ingredients = product.get_ingredients_with_quantity()
            quantity = ProductOrder.objects.get(product=product, order_id=self.id).quantity
            for ingredient, quantity_usage in ingredients:
                if ingredients_dictonary.get(ingredient.name):
                    ingredients_dictonary[ingredient.name] += quantity_usage * quantity
                else:
                    ingredients_dictonary = {**ingredients_dictonary, **{ingredient.name: quantity * quantity_usage}}

        return ingredients_dictonary


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        self.order.recalculate_total_price()

    def __str__(self):
        return f"Zamowienie: {self.order.id} - {self.product} x{self.quantity}"


class Table(models.Model):
    table_number = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    chairs_quantity = models.IntegerField(default=2)

    def __str__(self):
        return f"Stolik: {self.table_number} - {self.restaurant}"

    def is_free(self, date, reservation_start, reservation_end):
        reservations = Reservation.objects.filter(table_id=self.id, date=date)
        for reservation in reservations:
            start = reservation.time_start.replace(tzinfo=None)
            end = reservation.time_end.replace(tzinfo=None)

            if (reservation_start >= start and reservation_end <= end) or (
                    reservation_end > start and reservation_end <= end) or (
                    reservation_start >= start and reservation_start < end) or (
                    reservation_start <= start and reservation_end >= end):
                return False
        return True

    def make_reservation(self, client_name, client_phone, reservation_start, reservation_end):
        if self.is_free(reservation_start, reservation_end):
            reservation = Reservation.objects.create(client_name=client_name, client_phone=client_phone,
                                                     date_start=reservation_start, date_end=reservation_end,
                                                     table_id=self.id)
            reservation.save()
            print("Zarezerwowano stolik")
        else:
            print("Stolika nie mozna zarezerwowac")


class Reservation(models.Model):
    client_name = models.CharField(max_length=100)
    client_phone = models.CharField(max_length=100)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    time_start = models.TimeField(default=datetime.datetime.now().replace(tzinfo=None))
    time_end = models.TimeField(default=datetime.datetime.now().replace(tzinfo=None))

    def __str__(self):
        return f"Stolik {self.table} ({self.date.strftime('%Y-%m-%d')}) ({self.time_start.strftime('%H:%M')} - {self.time_end.strftime('%H:%M')}) - {self.client_name} (tel. {self.client_phone})"
