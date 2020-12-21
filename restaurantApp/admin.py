from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Product)
admin.site.register(Ingredient)
admin.site.register(ProductIngredient)
admin.site.register(Storage)
admin.site.register(Person)
admin.site.register(Employee)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(ProductOrder)
admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(Reservation)