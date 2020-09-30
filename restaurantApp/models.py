from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
import datetime

def time_in_between(now, start, end):
    if start <= end:
        return start >= now > end
    else:
        return start <= now or now < end

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    QUANTITY_TYPES = (
        ('GR', 'Gramy'),
        ('SZT', 'Sztuki')
    )
    quantity_type = models.CharField(max_length=3, choices=QUANTITY_TYPES, default='GR')

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
            return f"{self.street_name} {self.street_number}/{self.house_number}"
        else:
            return f"{self.street_name} {self.street_number}"


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

class Storage(models.Model):
    #     field for restaurant id
    # TODO del default
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()


    def __str__(self):
        return f"{self.restaurant} - {self.ingredient.name} ({self.quantity} {self.ingredient.quantity_type})"

    def save(self, *args, **kwargs):
        self.quantity = round(self.quantity, 2)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

    PRODUCT_TYPES = (
        ('N', 'Napój'),
        ('P', 'Posiłek')
    )
    product_type = models.CharField(max_length=3, choices=PRODUCT_TYPES, default='P')

    def __str__(self):
        return f"{self.name} ({self.price})"


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

    def __str__(self):
        return f"Zamowienie: {self.id}"

    def close_order(self, payment_method):
        if self.status == 'A':
            self.status = 'Z'
            self.payment = payment_method
            restaurant = Restaurant.objects.get(employee=self.employee)
            products_order = ProductOrder.objects.all().filter(order_id=self.id)
            for product in products_order:
                product_ingredients = ProductIngredient.objects.filter(product=product.product)
                for product_ingredient in product_ingredients:
                    ingredient = product_ingredient.ingredient
                    quantity = product_ingredient.quantity_usage
                    storage = Storage.objects.get(ingredient=ingredient, restaurant=restaurant)
                    storage.quantity -= quantity
                    storage.save()
            super().save()


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

    def __str__(self):
        return f"Stolik: {self.table_number} - {self.restaurant}"

    def is_free(self, time):
        reservations = Reservation.objects.filter(table_id=self.id)
        for reservation in reservations:
            start = reservation.date_start.strftime("%H:%M:%S")
            end = reservation.date_end.strftime("%H:%M:%S")
            # current_time = datetime.datetime.now()
            current_time = time
            print(type(time))
            print("Current Time =", current_time)

            print("Start =", start)
            print("End =", end)
            if time_in_between(current_time, start, end) == False:
                print("Stolik zajety")
            else:
                print("Stolik wolny")
            # print(reservation.date_start)



class Reservation(models.Model):
    client_name = models.CharField(max_length=100)
    client_phone = models.CharField(max_length=100)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
