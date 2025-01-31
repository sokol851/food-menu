from django.urls import path

from menu.apps import MenuConfig
from menu.views import FoodListAPIView

app_name = MenuConfig.name

urlpatterns = [
    path('api/v1/foods/', FoodListAPIView.as_view(), name='food-list'),
]
