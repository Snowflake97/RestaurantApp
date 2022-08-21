from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from restaurantApp.models import *
from scripts import functions


def manager_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.employee.position != "M":
            return HttpResponse('Nie posiadasz uprawnień')
        else:
            return view_func(request, *args, **kwargs)

    return _wrapped_view_func


# Create your views here.


def index(request):
    return render(request, "restaurantApp/index.html", None)


def product_list(request):
    products = Product.objects.all()
    products_ingredients = ProductIngredient.objects.all()
    return_directory = {"products": products, "products_ingredients": products_ingredients}
    return render(request, "restaurantApp/products.html", context=return_directory)


@login_required
def special(request):
    return HttpResponse("You are logged in. Nice!")


@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


def thx(request):
    return render(request, "restaurantApp/thx.html")


def signin(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                print(remember_me)
                if not remember_me:
                    request.session.set_expiry(0)
                    print("set expiry")
                return HttpResponseRedirect(reverse('restaurantApp:index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'restaurantApp/signin.html', {})


@login_required
def controll_panel(request):
    return render(request, "restaurantApp/controll_panel.html", None)


@login_required
@manager_required
def manager_panel(request):
    default_restaurant_id = request.user.employee.restaurant_id
    return render(request, "restaurantApp/manager_panel.html", {"restaurant_id": default_restaurant_id})


@login_required
def new_order(request):
    current_employee = request.user.employee
    order = Order.objects.create(employee=current_employee, date=datetime.datetime.now(), total_price=0, status='A')
    order.save()
    return redirect(f'/order/{order.id}')


@login_required
def active_orders(request):
    active_orders = Order.objects.filter(status='A')
    return render(request, "restaurantApp/active_orders.html", {"active_orders": active_orders})


def manage_orders(request):
    employee = request.user.employee
    active_employee_orders = Order.objects.filter(employee=employee, status="A")
    closed_employee_orders = Order.objects.filter(employee=employee, status="Z")
    return render(request, "restaurantApp/manage_orders.html",
                  {"active_orders": active_employee_orders, "closed_orders": closed_employee_orders})


@login_required
def order_detail(request, id):
    order_detail = Order.objects.get(id=id)
    products_order = ProductOrder.objects.filter(order_id=id)
    employee = request.user.employee
    active_employee_orders = Order.objects.filter(employee=employee, status="A")
    closed_employee_orders = Order.objects.filter(employee=employee, status="Z")
    return render(request, "restaurantApp/manage_orders.html",
                  {"order_detail": order_detail, "products_order": products_order,
                   "active_orders": active_employee_orders, "closed_orders": closed_employee_orders})


@login_required
def delete_order(request, id):
    Order.objects.get(id=id).delete()
    return redirect("/manage_orders/")


@login_required
def edit_product_order(request, id):
    product_order = ProductOrder.objects.get(id=id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        print(type(quantity))
        if quantity == 0:
            product_order.delete()
        else:
            product_order.quantity = quantity
            product_order.save()
        return redirect(f'/order/{product_order.order.id}')
    else:
        return render(request, "restaurantApp/edit_product_order.html", {"product_order": product_order})


@login_required
def client_form(request, restaurant_id, reservation_date, time_start, time_end, table_id):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        table = Table.objects.get(id=table_id)
        if table.is_free(reservation_date, time_start, time_end):
            reservation = Reservation.objects.create(client_name=name, client_phone=phone, table=table,
                                                     date=reservation_date, time_start=time_start, time_end=time_end)
            reservation.save()
        return render(request, "restaurantApp/index.html")
    else:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        table = Table.objects.get(id=table_id)
        print(reservation_date)
        print(type(time_start))
        return render(request, "restaurantApp/client_form.html",
                      {"restaurant": restaurant, "reservation_date": reservation_date, "time_start": time_start,
                       "time_end": time_end, "table": table})


@login_required
def products_group(request):
    # ingredient_types = IngredientType.objects.all()
    meals = Product.objects.filter(product_type='P')
    return render(request, "restaurantApp/manage_products.html", {"data": meals, "type": "meals"})


@login_required
def get_products(request, type="meals"):
    if type == "meals":
        meals = Product.objects.filter(product_type='P')
        return render(request, "restaurantApp/manage_products.html",
                      {"data": meals, "type": type})
    elif type == "beverages":
        beverages = Product.objects.filter(product_type='N')
        return render(request, "restaurantApp/manage_products.html",
                      {"data": beverages, "type": type})
    else:
        products = Product.objects.all()
        products_with_ingredient_type = []
        ingredient_type = type
        for product in products:
            if product.is_ingredient_type_in_product(ingredient_type):
                products_with_ingredient_type.append(product)
        return render(request, "restaurantApp/manage_products.html",
                      {"data": products_with_ingredient_type, "type": type})


@login_required
def order_add_product(request, id, type="meals"):
    if type == "meals":
        meals = Product.objects.filter(product_type='P')
        return render(request, "restaurantApp/order_add_product.html",
                      {"data": meals, "id": id, "type": type})
    elif type == "beverages":
        beverages = Product.objects.filter(product_type='N')
        return render(request, "restaurantApp/order_add_product.html",
                      {"data": beverages, "id": id, "type": type})
    else:
        products_with_ingredient_type = []
        ingredient_type = type
        products = Product.objects.all()
        for product in products:
            if product.is_ingredient_type_in_product(ingredient_type):
                products_with_ingredient_type.append(product)
        return render(request, "restaurantApp/order_add_product.html",
                      {"data": products_with_ingredient_type, "id": id, "type": type})


@login_required
def reservation(request):
    restaurants = Restaurant.objects.all()
    if request.method == "POST":
        restaurant_id = request.POST.get('restaurant')
        restaurant = Restaurant.objects.get(id=restaurant_id)
        date = request.POST.get('date')
        time_start = request.POST.get('time_start')
        time_start = functions.str_to_time_conversion(time_start)
        time_end = request.POST.get('time_end')
        time_end = functions.str_to_time_conversion(time_end)

        free_tables = []
        tables = Table.objects.filter(restaurant_id=restaurant_id)
        for table in tables:
            if table.is_free(date, time_start, time_end):
                free_tables.append(table)
        return render(request, "restaurantApp/reservation.html",
                      {"tables": free_tables, "restaurant": restaurant, "id": restaurant_id,
                       "reservation_date": date, "time_start": time_start, "time_end": time_end,
                       "restaurants": restaurants})

        # return render(request, "restaurantApp/reservation.html", {"restaurants":restaurants})

    return render(request, "restaurantApp/reservation.html", {"restaurants": restaurants})


@login_required
def new_product(request, product_type):
    ingredients = Ingredient.objects.all()
    if request.method == "POST":
        product_name = request.POST.get("product-name")
        product_price = float(request.POST.get("product-price"))
        # product_type = request.POST.get("product-type")
        product = Product.objects.create(name=product_name, price=product_price, product_type=product_type)
        product.save()

        for ing in ingredients:
            ing_id = request.POST.get(f"ID:{ing.name}")
            ing_quantity = request.POST.get(f"QUANTITY:{ing.name}")
            if ing_id != None:
                ingredient = Ingredient.objects.get(id=ing_id)
                product_ingredient = ProductIngredient.objects.create(product=product, ingredient=ingredient,
                                                                      quantity_usage=int(ing_quantity))
                product_ingredient.save()

        return redirect("/products_group/")
    return render(request, "restaurantApp/new_product.html", {"ingredients": ingredients, "product_type": product_type})


@login_required
def order_add_beverage(request, id):
    beverages = Product.objects.filter(product_type='N')
    return render(request, "restaurantApp/order_add_product.html", {"data": beverages, "id": id})


@login_required
def order_id_add_product_id(request, id, product_id):
    order = Order.objects.get(id=id)
    quantity = 1
    product = Product.objects.get(id=product_id)
    order.add_product(product, quantity)

    return redirect(f'/order/{order.id}/')


@login_required
def edit_product(request, id):
    all_ingredients = Ingredient.objects.all()
    if request.method == "POST":
        product_name = request.POST.get("product-name")
        product_price = float(request.POST.get("product-price"))
        product_type = request.POST.get("product-type")
        product = Product.objects.get(name=product_name, price=product_price, product_type=product_type)
        product.name = product_name
        product.price = product_price
        product.product_type = product_type
        product.save()
        checked_ids = []
        all_ids = []
        for ing in all_ingredients:
            all_ids.append(ing.id)
            ing_id = request.POST.get(f"ID:{ing.name}")
            ing_quantity = request.POST.get(f"QUANTITY:{ing.name}")
            if ing_id != None:
                checked_ids.append(int(ing_id))
                product_ingredient, created = ProductIngredient.objects.get_or_create(product=product,
                                                                                      ingredient_id=ing_id)
                if ing_quantity == "0":
                    product_ingredient.delete()
                else:
                    product_ingredient.quantity_usage = ing_quantity
                    product_ingredient.save()
        for id in all_ids:
            if id not in checked_ids:
                product_to_delete = ProductIngredient.objects.filter(product=product, ingredient_id=id)
                if product_to_delete:
                    product_to_delete.delete()

        return redirect(f'/products_group/meals/')
    else:
        ingredients = []
        product = Product.objects.get(id=id)
        product_ingredients = list(product.get_ingredients_with_quantity())
        product_ingredients_dictonary = {}
        all_ingredients_dictonary = {}
        for ing, quantity in product_ingredients:
            product_ingredients_dictonary = {**product_ingredients_dictonary, ing: quantity}
        for ing in all_ingredients:
            all_ingredients_dictonary = {**all_ingredients_dictonary, ing: 0}

        pass_dict = {**all_ingredients_dictonary, **product_ingredients_dictonary}

        for ing in pass_dict:
            ingredients.append((ing, pass_dict[ing]))
        return render(request, "restaurantApp/edit_product.html",
                      {"product": product, "ingredients": ingredients})


@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect(f'/products_group/')


@login_required
def close_order(request, id):
    if request.method == "POST":
        order = Order.objects.get(id=id)
        payment_type = request.POST.get("payment_type")
        order.close_order(payment_type)
        # order.payment = payment_type
        # order.save()

    return redirect(f'/controll_panel/')


@login_required
def check_user(request):
    if request.is_ajax and request.method == "GET":
        username = request.GET.get("username", None)
        if User.objects.filter(username=username).exists():
            # if nick_name found return not valid new friend
            return JsonResponse({"valid": False})
        else:
            # if nick_name not found, then user can create a new friend.
            return JsonResponse({"valid": True})

    return JsonResponse({})


@login_required
@manager_required
def create_restaurant(request):
    if request.method == "POST":
        street_name = request.POST.get("street_name")
        street_number = request.POST.get("street_number")
        house_number = request.POST.get("house_number")
        zip_code = request.POST.get("zip_code")
        city = request.POST.get("city")

        address = Address.objects.create(street_name=street_name, street_number=street_number, city=city,
                                         zip_code=zip_code)
        if house_number:
            address.house_number = house_number
        address.save()

        restaurant = Restaurant.objects.create(address=address)
        restaurant.save()

        return redirect(f'/controll_panel/')

    return render(request, "restaurantApp/create_restaurant.html", {})


@login_required
@manager_required
def manage_ingredients(request, type="all"):
    if type == "all":
        ingredients = Ingredient.objects.all()
    else:
        ingredients = Ingredient.objects.filter(ingredient_type=type)
    return render(request, "restaurantApp/manage_ingredients.html",
                  {"data": ingredients})


@login_required
@manager_required
def add_ingredient(request):
    if request.method == "POST":
        ingredient_name = request.POST.get("ingredient_name")
        ingredient_type = request.POST.get("ingredient_type")
        ingredient_quantity = request.POST.get("ingredient_quantity")
        ingredient = Ingredient.objects.create(name=ingredient_name, quantity_type=ingredient_quantity,
                                               ingredient_type=ingredient_type)
        ingredient.save()
        return redirect('/manage_ingredients/all/')
    return render(request, "restaurantApp/create_ingredient.html", {})


@login_required
@manager_required
def delete_ingredient(request, id):
    ingredient = Ingredient.objects.get(id=id)
    ingredient.delete()
    return redirect('/manage_ingredients/all/')


@login_required
@manager_required
def manage_employees(request, id=-1):
    restaurants = Restaurant.objects.all()
    if id != 0:
        restaurant = Restaurant.objects.get(id=id)
        emplyees = Employee.objects.filter(restaurant=restaurant)
        return render(request, "restaurantApp/manage_employees.html",
                      {"restaurants": restaurants, "emplyees": emplyees})
    return render(request, "restaurantApp/manage_employees.html", {"restaurants": restaurants})


@login_required
@manager_required
def create_user(request):
    restuarants = Restaurant.objects.all()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        street_name = request.POST.get("street_name")
        street_number = request.POST.get("street_number")
        house_number = request.POST.get("house_number")
        zip_code = request.POST.get("zip_code")
        city = request.POST.get("city")
        position = request.POST.get("position")
        restuarant_id = request.POST.get("restaurant")
        restuarant = Restaurant.objects.get(id=restuarant_id)

        user = User.objects.create(username=username, password=password)
        user.set_password(password)
        user.save()

        address = Address.objects.create(street_name=street_name, street_number=street_number, city=city,
                                         zip_code=zip_code)
        if house_number:
            address.house_number = house_number
        address.save()

        person = Person.objects.create(first_name=first_name, last_name=last_name, phone_number=phone_number,
                                       address=address)
        person.save()

        employee = Employee.objects.create(person=person, user=user, restaurant=restuarant, position=position)
        employee.save()

        return redirect(f'/manage_employees/restaurant/0/')

    return render(request, "restaurantApp/create_employee.html", {"restuarants": restuarants})


@login_required
@manager_required
def delete_employee(request, id):
    employee = Employee.objects.get(id=id)
    employee.user.delete()
    employee.delete()
    employee.person.address.delete()
    employee.person.delete()
    return redirect("/manage_employees/restaurant/0/")


@login_required
@manager_required
def edit_employee(request, id):
    employee = Employee.objects.get(id=id)
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        street_name = request.POST.get("street_name")
        street_number = request.POST.get("street_number")
        house_number = request.POST.get("house_number")
        zip_code = request.POST.get("zip_code")
        city = request.POST.get("city")
        position = request.POST.get("position")

        person = employee.person
        person.phone_number = phone_number
        person.save()

        address = person.address
        address.street_name = street_name
        address.street_number = street_number
        if house_number:
            address.house_number = house_number
        address.zip_code = zip_code
        address.city = city
        address.save()

        employee.position = position
        employee.save()

        return redirect("/manage_employees/restaurant/0/")

    return render(request, "restaurantApp/edit_employee.html", {"employee": employee})


@login_required
@manager_required
def employee_set_password(request, id):
    employee = Employee.objects.get(id=id)
    if request.method == "POST":
        password = request.POST.get('password')
        employee.user.set_password(password)
        employee.user.save()
        employee.save()

        return redirect("/manage_employees/restaurant/0/")

    return render(request, "restaurantApp/set_password_employee.html", {"employee": employee})


@login_required
@manager_required
def manage_restaurants(request, type, id=0):
    restaurants = Restaurant.objects.all()
    print(restaurants)
    if type == "M":
        if id != 0:
            restaurant = Restaurant.objects.get(id=id)
            storage = Storage.objects.filter(restaurant=restaurant)
            return render(request, "restaurantApp/manage_restaurants.html",
                          {"restaurants": restaurants, "restaurant": restaurant, "storage": storage})
    elif type == "S":
        if id != 0:
            restaurant = Restaurant.objects.get(id=id)
            tables = Table.objects.filter(restaurant=restaurant)
            return render(request, "restaurantApp/manage_restaurants.html",
                          {"restaurants": restaurants, "restaurant": restaurant, "tables": tables})
        pass

    return render(request, "restaurantApp/manage_restaurants.html",
                  {"restaurants": restaurants})


@login_required
@manager_required
def add_ingredient_to_storage(request, id):
    storage = Storage.objects.get(id=id)
    if request.method == "POST":
        quantity = request.POST.get('quantity')
        storage.add_quantity(int(quantity))
        restaurant_id = storage.restaurant.id
        return redirect(f"/manage_restaurants/M/{restaurant_id}/")
    return render(request, "restaurantApp/add_ingredient_to_storage.html", {"storage": storage})


@login_required
@manager_required
def edit_ingredient_to_storage(request, id):
    storage = Storage.objects.get(id=id)
    if request.method == "POST":
        quantity = request.POST.get('quantity')
        storage.edit_quantity(int(quantity))
        restaurant_id = storage.restaurant.id
        return redirect(f"/manage_restaurants/M/{restaurant_id}/")
    return render(request, "restaurantApp/edit_storage_ingredient.html", {"storage": storage})


@login_required
@manager_required
def edit_table(request, id):
    table = Table.objects.get(id=id)
    if request.method == "POST":
        table_number = request.POST.get('table_number')
        chairs_quantity = request.POST.get('chairs_quantity')
        table.table_number = table_number
        table.chairs_quantity = chairs_quantity
        table.save()
        restaurant_id = table.restaurant_id
        return redirect(f'/manage_restaurants/S/{restaurant_id}/')
    return render(request, "restaurantApp/edit_table.html", {"table": table})


@login_required
@manager_required
def delete_table(request, id):
    table = Table.objects.get(id=id)
    restaurant_id = table.restaurant_id
    table.delete()
    return redirect(f'/manage_restaurants/S/{restaurant_id}/')


@login_required
@manager_required
def add_table(request):
    restaurants = Restaurant.objects.all()
    if request.method == "POST":
        table_number = int(request.POST.get('table_number'))
        chairs_quantity = int(request.POST.get('chairs_quantity'))
        restaurant_id = int(request.POST.get('restaurant'))
        table = Table.objects.create(restaurant_id=restaurant_id, table_number=table_number,
                                     chairs_quantity=chairs_quantity)
        table.save()
        return redirect(f'/manage_restaurants/S/{restaurant_id}/')
    return render(request, "restaurantApp/create_table.html", {"restaurants": restaurants})


@login_required
@manager_required
def raports(request):
    restaurants = Restaurant.objects.all()
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        restaurant_id = request.POST.get('restaurant')
        restaurant = Restaurant.objects.get(id=restaurant_id)
        products = restaurant.get_products_from_time_period(start_date, end_date)
        ingredients = restaurant.get_ingredients_usage_from_time_period(start_date, end_date)
        income = restaurant.get_income_from_time_period(start_date, end_date)
        return render(request, "restaurantApp/raports.html",
                      {"restaurants": restaurants, "products": products, "ingredients": ingredients, "income": income})
    return render(request, "restaurantApp/raports.html", {"restaurants": restaurants})
