# import os
#
# os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
#
# import django
#
# django.setup()

from django.test import TestCase
from backend.restaurantApp.models import *


class MyTestCase(TestCase):
    def setUp(self):
        person_address = Address.objects.create(street_name="Person_address", street_number=0, house_number=0,
                                                zip_code="00-000", city="Test")
        restaurant_address = Address.objects.create(street_name="Restaurant_address", street_number=1, house_number=1,
                                                    zip_code="11-111", city="Test")
        person = Person.objects.create(first_name="Person_name", last_name="Person_last_name", phone_number="000000000",
                                       address=person_address)
        user = User.objects.create(username="Test_user", password="Test")
        restaurant = Restaurant.objects.create(address=restaurant_address)
        employee = Employee.objects.create(person=person, user=user, restaurant=restaurant, position="M")
        product = Product.objects.create(name="Kanpka z szynka", price=30.00, product_type="P")
        ingredient = Ingredient.objects.create(name="Szynka", quantity_type="GR")
        product_ingredient = ProductIngredient.objects.create(product=product, ingredient=ingredient,
                                                              quantity_usage=100)
        order = Order.objects.create(employee=employee)

    def test_new_ingredient(self):
        ingredient = Ingredient.objects.get(name="Szynka")
        self.assertEqual(ingredient.quantity_type, "GR")

    def test_ingredient_in_product(self):
        product = Product.objects.get(name="Kanpka z szynka")
        ingredient = Ingredient.objects.get(name="Szynka")
        self.assertEqual(product.get_ingredients()[0], ingredient)

    def test_order_add_prduct(self):
        order = Order.objects.last()
        product = Product.objects.get(name="Kanpka z szynka")
        order.add_product(product, 1)
        self.assertEqual(order.get_products()[0], product)

    def test_change_order_value_after_add_product(self):
        product = Product.objects.get(name="Kanpka z szynka")
        product_value = product.price
        quantity = 2

        order = Order.objects.last()
        order_value = order.total_price
        order.add_product(product, quantity)

        self.assertEqual(order.total_price, product_value * quantity + order_value)

    def test_close_order(self):
        order = Order.objects.last()
        order.close_order(payment_method="K")
        self.assertEqual(order.status, "Z")
        self.assertEqual(order.payment, "K")

    def test_default_storage_creation(self):
        storage = Storage.objects.last()
        restaurant = Restaurant.objects.last()
        ingredient = Ingredient.objects.last()
        self.assertEqual(storage.restaurant, restaurant)
        self.assertEqual(storage.ingredient, ingredient)
        self.assertEqual(storage.quantity, 0)

    def test_add_ingredient_to_storage(self, test_quantity=200):
        storage = Storage.objects.last()
        storage_quantity = storage.quantity
        storage.add_quantity(test_quantity)
        self.assertEqual(storage.quantity, storage_quantity + test_quantity)

    def test_add_ingredient_to_storage(self, test_quantity=200):
        storage = Storage.objects.last()
        storage.edit_quantity(test_quantity)
        self.assertEqual(storage.quantity, test_quantity)

    def test_close_order_decrement_storage_quantity(self, product_quantity=2, start_quantity=1000):
        order = Order.objects.last()
        restaurant = order.employee.restaurant
        product = Product.objects.get(name="Kanpka z szynka")
        ingredients = product.get_ingredients()

        for ingredient in ingredients:
            storage = Storage.objects.get(restaurant=restaurant, ingredient=ingredient)
            storage.edit_quantity(start_quantity)

        order.add_product(product, product_quantity)
        order.close_order(payment_method="K")

        self.assertEqual(order.status, "Z")
        self.assertEqual(order.payment, "K")

        for ingredient in ingredients:
            ingredient_usage = ProductIngredient.objects.get(ingredient=ingredient, product=product).quantity_usage
            storage = Storage.objects.get(restaurant=restaurant, ingredient=ingredient)
            self.assertEqual(storage.quantity, start_quantity - ingredient_usage * product_quantity)


if __name__ == '__main__':
    TestCase.main()
