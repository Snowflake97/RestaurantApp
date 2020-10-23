import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Inzynierka.settings'

import django

django.setup()

from restaurantApp.models import *
from datetime import datetime
import datetime


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


start_date = "2020-01-01"
end = "2020-12-30"

r = Restaurant.objects.get(id=1)
print(r.get_ingredients_usage_from_time_period(start_date, end))
print(r.get_income_from_time_period(start_date, end))
