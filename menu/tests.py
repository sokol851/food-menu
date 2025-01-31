from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from menu.models import Food, FoodCategory


class FoodListAPIViewTests(APITestCase):
    def setUp(self):
        """ Создаём тестовые данные """
        # Категория напитки
        self.category_drinks = FoodCategory.objects.create(
            name_ru="Напитки",
            order_id=10
        )
        # Опубликованные блюда в категории Напитки
        self.drink_tea = Food.objects.create(
            category=self.category_drinks,
            is_publish=True,
            is_vegan=False,
            is_special=False,
            code=1,
            internal_code=100,
            name_ru="Чай",
            description_ru="Чай 100 гр",
            cost=123.00
        )
        self.drink_cola = Food.objects.create(
            category=self.category_drinks,
            is_publish=True,
            is_vegan=False,
            is_special=False,
            code=2,
            internal_code=200,
            name_ru="Кола",
            description_ru="Кола",
            cost=123.00
        )
        # Не опубликованное блюдо в той же категории
        self.drink_hidden = Food.objects.create(
            category=self.category_drinks,
            is_publish=False,
            is_vegan=False,
            is_special=False,
            code=5,
            internal_code=500,
            name_ru="Сок",
            description_ru="Свежий сок",
            cost=150.00
        )

        # Категория выпечка
        self.category_bakery = FoodCategory.objects.create(
            name_ru="Выпечка",
            order_id=20
        )
        self.bakery_bread = Food.objects.create(
            category=self.category_bakery,
            is_publish=True,
            is_vegan=True,
            is_special=False,
            code=3,
            internal_code=300,
            name_ru="Хлеб",
            description_ru="Цельнозерновой хлеб",
            cost=50.00
        )

        # Категория салаты (нет опубликованных блюд)
        self.category_salads = FoodCategory.objects.create(
            name_ru="Салаты",
            order_id=30
        )
        self.salad_hidden = Food.objects.create(
            category=self.category_salads,
            is_publish=False,
            is_vegan=True,
            is_special=False,
            code=4,
            internal_code=400,
            name_ru="Цезарь",
            description_ru="Салат Цезарь",
            cost=200.00
        )

    def test_category_published_foods(self):
        """ Проверяем на возврат категорий с опубликованными блюдами """
        url = reverse('menu:food-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        category_names = [category['name_ru'] for category in response.data]
        self.assertIn("Напитки", category_names)
        self.assertIn("Выпечка", category_names)
        self.assertNotIn("Салаты", category_names)

    def test_list_foods_published(self):
        """ Проверяем, что в категории отображаются только опубликованные блюда """
        url = reverse('menu:food-list')
        response = self.client.get(url, format='json')

        for category in response.data:
            for food in category['foods']:
                food_obj = Food.objects.get(internal_code=food['internal_code'])
                self.assertTrue(food_obj.is_publish)

    def test_empty_list(self):
        """ Проверяем что API возвращает пустой список, если нет категорий с опубликованными блюдами """
        # Скрываем все опубликованные блюда
        Food.objects.filter(is_publish=True).update(is_publish=False)

        url = reverse('menu:food-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
