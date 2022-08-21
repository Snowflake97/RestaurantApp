from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "apiApp"

# create router for backend api
apiRouter = routers.DefaultRouter()
apiRouter.register(r'users', views.UserViewSet)
apiRouter.register(r'groups', views.GroupViewSet)

# urls provided by the backend
urlpatterns = [
    path('api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),
    path('', include(apiRouter.urls)),
]
