from django.contrib import admin

from menu.models import Food, FoodCategory


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    """ Админ-модель категорий """
    list_display = (
        "name_ru",
        "order_id",
    )
    ordering = (
        'name_ru',
    )
    search_fields = (
        "name_ru",
        "name_en",
        "name_ch",
        "order_id",
    )


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    """ Админ-модель блюд """
    list_display = (
        "name_ru",
        "cost",
        "category",
        "is_vegan",
        "is_special",
        "code",
        "internal_code",
        "is_publish",
    )
    ordering = (
        'internal_code',
    )
    list_filter = (
        "category",
        "is_vegan",
        "is_special",
        "code",
        "internal_code",
        "is_publish",
    )
    search_fields = (
        "name_ru",
        "category__order_id",
        "category__name_ru",
        "code",
        "internal_code",
    )
