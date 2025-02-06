from django.db.models import Prefetch
from rest_framework import generics

from menu.models import Food, FoodCategory
from menu.serializers import FoodListSerializer


class FoodListAPIView(generics.ListAPIView):
    """ Получение списка категорий блюд с опубликованными блюдами. """
    serializer_class = FoodListSerializer

    def get_queryset(self):
        # Фильтр только опубликованных блюд
        # Использование select_related для объединения запросов и prefetch_related для кеширования допов.
        published_foods = Food.objects.select_related('category').filter(is_publish=True).prefetch_related(
            'additional')

        # Сортировка по коду в приложении
        published_foods = published_foods.order_by('internal_code')

        # Фильтр категорий, у которых есть хотя бы одно опубликованное блюдо
        queryset = FoodCategory.objects.filter(food__is_publish=True).distinct()

        # Предварительно загружаем только опубликованные блюда для каждой категории
        # Использование Prefetch для уменьшения количества обращений к базе данных
        queryset = queryset.prefetch_related(
            Prefetch('food', queryset=published_foods)
        )

        # Сортируем категории по order_id
        queryset = queryset.order_by('order_id')

        return queryset
