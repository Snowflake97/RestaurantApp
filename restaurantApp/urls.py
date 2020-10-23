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
    # path('register/', views.register, name="register"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.user_logout, name="logout"),
    path('thx/', views.thx, name="thx"),
    path('controll_panel/', views.controll_panel, name="controll_panel"),
    path('controll_panel/new_product/<str:product_type>/', views.new_product, name="new_product"),
    path('products_group/edit_product/<int:id>/', views.edit_product, name="edit_product"),
    path('products_group/delete_product/<int:id>/', views.delete_product, name="delete_product"),
    path('new_order/', views.new_order, name="new_order"),
    path('active_orders/', views.active_orders, name="active_orders"),
    path('products_group/', views.products_group, name="products_group"),
    path('products_group/melas/', views.get_meals, name="get_meals"),
    path('products_group/beverages/', views.get_beverages, name="get_beverages"),
    path('order/<int:id>/', views.order_detail, name='order_detail'),
    path('order/<int:id>/delete', views.delete_order, name='delete_order'),
    path('order/<int:id>/edit', views.edit_product_order, name='edit_product_order'),
    path('order/<int:id>/add_product', views.order_add_product, name='order_add_product'),
    path('order/<int:id>/add_product/meals/', views.order_add_meal, name='order_add_meal'),
    path('order/<int:id>/add_product/beverages/', views.order_add_beverage, name='order_add_beverage'),
    path('order/<int:id>/add_product/meals/<int:product_id>', views.order_id_add_product_id,
         name='order_id_add_product_id'),
    # path('reservation/', views.DateCreateView.as_view(), name='reservation'),
    # path('reservation/<int:restaurant_id>/<year:reservation_date>/<time:time_start>/<time:time_end>/',
    #      views.tables_view, name='tables_view'),
    path('reservation/<int:restaurant_id>/<year:reservation_date>/<time:time_start>/<time:time_end>/<int:table_id>/',
         views.client_form, name='client_form'),
    path('reservation/', views.reservation, name='reservation')
]
