from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Storage(models.Model):
    #     field for restaurant id
    #   restaurant = models.ForeignKey(Restaurant)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    QUANTITY_TYPES = (
        ('KG', 'Kilogramy'),
        ('DG', 'Dekagramy'),
        ('GR', 'Gramy'),
        ('SZT', 'Sztuki')
    )
    quantity_type = models.CharField(max_length=3, choices=QUANTITY_TYPES)

    def __str__(self):
        return f"{self.ingredient.name} ({self.quantity} {self.quantity_type})"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.price})"


class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_usage = models.IntegerField()

    QUANTITY_TYPES = (
        ('KG', 'Kilogramy'),
        ('DG', 'Dekagramy'),
        ('GR', 'Gramy'),
        ('SZT', 'Sztuki')
    )
    quantity_type = models.CharField(max_length=3, choices=QUANTITY_TYPES)

    def __str__(self):
        return f"{self.product.name} - {self.ingredient.name} ({self.quantity_usage} {self.quantity_type})"


class Address(models.Model):
    street_name = models.CharField(max_length=100)
    street_number = models.IntegerField()
    house_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.house_number:
            return f"{self.street_name} {self.street_number}/{self.house_number}"
        else:
            return f"{self.street_name} {self.street_number}"


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
    POSITIONS = (
        ('M', 'Manager'),
        ('W', 'Worker')
    )
    position = models.CharField(max_length=1, choices=POSITIONS)

    def __str__(self):
        return f"{self.person} ({self.get_position_display()})"


class Order(models.Model):
    date = models.DateTimeField(default=timezone.now)
    # employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return f"Zamowienie: {self.id}"

#     ???????

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.order.total_price += self.product.price * self.quantity
        self.order.save()
        super().save()

    def __str__(self):
        return f"Zamowienie: {self.order.id} - {self.product} x{self.quantity}"
