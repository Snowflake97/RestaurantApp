from django.urls import path, include
from django.urls import path, register_converter
import functions
import datetime
from . import views

app_name = "restaurantApp"


class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value


class TimeConverter:
    regex = '\d{2}:\d{2}:\d{2}'

    def to_python(self, value):
        time = functions.str_to_time_conversion(value)
        return time

    def to_url(self, value):
        return datetime.time.strftime(value, '%H:%M:%S')


register_converter(DateConverter, 'year')
register_converter(TimeConverter, 'time')

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.product_list, name="products"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.user_logout, name="logout"),
    path('thx/', views.thx, name="thx"),
    path('controll_panel/', views.controll_panel, name="controll_panel"),
    path('controll_panel/create_user/', views.create_user, name="create_user"),
    path('controll_panel/check_user/', views.check_user, name="check_user"),
    path('controll_panel/new_product/<str:product_type>/', views.new_product, name="new_product"),

    path('manager_panel/', views.manager_panel, name="manager_panel"),
    path('manager_panel/create_restaurant', views.create_restaurant, name="create_restaurant"),

    path('products_group/edit_product/<int:id>/', views.edit_product, name="edit_product"),
    path('products_group/delete_product/<int:id>/', views.delete_product, name="delete_product"),
    path('products_group/', views.products_group, name="products_group"),
    path('products_group/<str:type>/', views.get_products, name="get_products"),

    path('manage_ingredients/<str:type>/', views.manage_ingredients, name="manage_ingredients"),
    path('manage_employees/restaurant/<int:id>/', views.manage_employees, name="manage_employees"),
    path('manage_employees/delete_employee/<int:id>/', views.delete_employee, name="delete_employee"),
    path('manage_employees/edit_employee/<int:id>/', views.edit_employee, name="edit_employee"),
    path('manage_employees/set_password/<int:id>/', views.employee_set_password, name="employee_set_password"),

    path('manage_restaurants/<str:type>/<int:id>/', views.manage_restaurants, name="manage_restaurants"),
    path('manage_restaurants/restaurant/add_ingredient_to_storage/<int:id>/', views.add_ingredient_to_storage,
         name="add_ingredient_to_storage"),
    path('manage_restaurants/restaurant/edit_ingredient_to_storage/<int:id>/', views.edit_ingredient_to_storage,
         name="edit_ingredient_to_storage"),

    path('manage_orders/', views.manage_orders, name="manage_orders"),

    path('raports/', views.raports, name="raports"),

    path('add_table/', views.add_table, name="add_table"),
    path('edit_table/<int:id>/', views.edit_table, name="edit_table"),
    path('delete_table/<int:id>/', views.delete_table, name="delete_table"),

    path('add_ingredient/', views.add_ingredient, name="add_ingredient"),
    path('delete_ingredient/<int:id>/', views.delete_ingredient, name="delete_ingredient"),

    path('new_order/', views.new_order, name="new_order"),

    path('active_orders/', views.active_orders, name="active_orders"),

    path('order/<int:id>/', views.order_detail, name='order_detail'),

    path('order/<int:id>/close/', views.close_order, name='close_order'),
    path('order/<int:id>/delete', views.delete_order, name='delete_order'),
    path('order/<int:id>/edit', views.edit_product_order, name='edit_product_order'),
    path('order/<int:id>/add_product/<str:type>/', views.order_add_product, name='order_add_product'),

    path('order/<int:id>/add_product/<int:product_id>', views.order_id_add_product_id,
         name='order_id_add_product_id'),

    path('reservation/<int:restaurant_id>/<year:reservation_date>/<time:time_start>/<time:time_end>/<int:table_id>/',
         views.client_form, name='client_form'),
    path('reservation/', views.reservation, name='reservation'),
]
