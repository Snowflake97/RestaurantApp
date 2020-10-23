from django.shortcuts import render
from restaurantApp.models import Product, ProductIngredient, Order, ProductOrder
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from restaurantApp.forms import *
from django.views.generic.edit import FormView, View
import datetime
import functions


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
    return HttpResponseRedirect(reverse("restaurantApp:thx"))


def thx(request):
    return render(request, "restaurantApp/thx.html")


# def register(request):
#     registered = False
#
#     if request.method == "POST":
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileInfoForm(data=request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             if 'profile_pic' in request.FILES:
#                 profile.profile_pic = request.FILES['profile_pic']
#
#             profile.save()
#
#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileInfoForm()
#
#     return render(request, 'user_app/register.html',
#                   context={"registered": registered,
#                            "user_form": user_form,
#                            "profile_form": profile_form})


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
def new_order(request):
    current_employee = request.user.employee
    order = Order.objects.create(employee=current_employee, date=datetime.datetime.now(), total_price=0, status='A')
    order.save()
    return redirect(f'/order/{order.id}')


@login_required
def active_orders(request):
    active_orders = Order.objects.filter(status='A')
    return render(request, "restaurantApp/active_orders.html", {"active_orders": active_orders})


@login_required
def order_detail(request, id):
    order_detail = Order.objects.get(id=id)
    products_order = ProductOrder.objects.filter(order_id=id)
    return render(request, "restaurantApp/order_detail.html",
                  {"order_detail": order_detail, "products_order": products_order})


@login_required
def delete_order(request, id):
    Order.objects.get(id=id).delete()
    return render(request, "restaurantApp/controll_panel.html", None)


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
def order_add_product(request, id):
    products = Product.objects.all()
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        product = Product.objects.get(id=product_id)
        order.add_product(product, quantity)

        return redirect(f'/order/{order.id}')

    return render(request, "restaurantApp/order_add_product.html", {"products": products, "id": id})


# class DateCreateView(FormView):
#     template_name = 'restaurantApp/reservation.html'
#     form_class = ReservationForm
#     success_url = '/thx/'
#
#     def form_valid(self, form):
#         # date = form.cleaned_data['date']
#         # time_start = form.cleaned_data['time_start']
#         # time_end = form.cleaned_data['time_end']
#         # table = Table.objects.last()
#         return super(DateCreateView, self).form_valid(form)
#
#     def post(self, request, *args, **kwargs):
#         restaurant_id = request.POST.get('restaurant')
#         date = request.POST.get('date')
#         time_start = request.POST.get('time_start')
#         time_start = functions.str_to_time_conversion(time_start)
#         time_end = request.POST.get('time_end')
#         time_end = functions.str_to_time_conversion(time_end)
#         return redirect(f'/reservation/{restaurant_id}/{date}/{time_start}/{time_end}')
#
#     def get(self, request, *args, **kwargs):
#         restaurants = Restaurant.objects.all()
#         return render(request, "restaurantApp/reservation.html", {"restaurants": restaurants})

#
# def tables_view(request, restaurant_id, reservation_date, time_start, time_end):
#     restaurant = Restaurant.objects.get(id=restaurant_id)
#     reservation_date = reservation_date.date()
#     free_tables = []
#     tables = Table.objects.filter(restaurant_id=restaurant_id)
#     for table in tables:
#         if table.is_free(reservation_date, time_start, time_end):
#             free_tables.append(table)
#     return render(request, "restaurantApp/free_tables.html",
#                   {"tables": free_tables, "restaruant": restaurant, "id": restaurant_id,
#                    "reservation_date": reservation_date, "time_start": time_start, "time_end": time_end})


def client_form(request, restaurant_id, reservation_date, time_start, time_end, table_id):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        table = Table.objects.get(id=table_id)
        if table.is_free(reservation_date, time_start, time_end):
            reservation = Reservation.objects.create(client_name=name, client_phone=phone, table=table,
                                                     date=reservation_date, time_start=time_start, time_end=time_end)
            reservation.save()
        return render(request, "restaurantApp/thx.html")
    else:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        table = Table.objects.get(id=table_id)
        print(reservation_date)
        print(type(time_start))
        return render(request, "restaurantApp/client_form.html",
                      {"restaurant": restaurant, "reservation_date": reservation_date, "time_start": time_start,
                       "time_end": time_end, "table": table})


def products_group(request):
    meals = Product.objects.filter(product_type='P')
    return render(request, "restaurantApp/products_group.html", {"data": meals})


def get_meals(request):
    meals = Product.objects.filter(product_type='P')
    return render(request, "restaurantApp/products_group.html", {"data": meals})


def get_beverages(request):
    beverages = Product.objects.filter(product_type='N')
    return render(request, "restaurantApp/products_group.html", {"data": beverages})


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

        return render(request, "restaurantApp/products.html")
    return render(request, "restaurantApp/new_product.html", {"ingredients": ingredients, "product_type": product_type})


def order_add_meal(request, id):
    meals = Product.objects.filter(product_type='P')
    return render(request, "restaurantApp/order_add_product.html", {"data": meals, "id": id})


def order_add_beverage(request, id):
    beverages = Product.objects.filter(product_type='N')
    return render(request, "restaurantApp/order_add_product.html", {"data": beverages, "id": id})


def order_id_add_product_id(request, id, product_id):
    order = Order.objects.get(id=id)
    quantity = 1
    product = Product.objects.get(id=product_id)
    order.add_product(product, quantity)

    return redirect(f'/order/{order.id}/')


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

        return redirect(f'/products_group/melas/')
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

def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect(f'/products_group/melas/')