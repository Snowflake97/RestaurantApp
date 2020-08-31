from django.urls import path, include
from . import views

app_name = "restaurantApp"

urlpatterns = [
    path("", views.index, name="index")
]
