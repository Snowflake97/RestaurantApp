import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Inzynierka.settings'

import django

django.setup()

from restaurantApp.models import *
from datetime import datetime


def printProductsByIngredient(ingredientName):
    productIngriedient = ProductIngredient.objects.all().filter(ingredient__name=ingredientName)

    for meal in productIngriedient:
        print(meal.product)


# printProductsByIngredient("Cheese")

def printProductWithIngriedients(productName):
    print(f"{productName}: ")
    productIngriedient = ProductIngredient.objects.all().filter(product__name=productName)

    for meal in productIngriedient:
        print(f"- {meal.ingredient}")


# printProductWithIngriedients("Sandwitch")
# product = Product.objects.last()
# order = Order.objects.get(id=1)
# order.add_product(product, 1)
# print(order.get_products())
# print(order.get_price())
# order.close_order('K')

# for order in Order.objects.all():
#     print(order.employee)


table = Table.objects.get(id=1)
c = datetime(hour = 11, minute = 34, second=12)
print(c)
print(type(c))
table.is_free(c)
print(table)