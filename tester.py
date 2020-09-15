import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Inzynierka.settings'

import django

django.setup()

from restaurantApp.models import *

def printProductsByIngredient(ingredientName):
    productIngriedient = ProductIngredient.objects.all().filter(ingredient__name = ingredientName)

    for meal in productIngriedient:
        print(meal.product)

printProductsByIngredient("Cheese")

def printProductWithIngriedients(productName):
    print(f"{productName}: ")
    productIngriedient = ProductIngredient.objects.all().filter(product__name = productName)
    for meal in productIngriedient:
        print(f"- {meal.ingredient}")

printProductWithIngriedients("Sandwitch")