from django.contrib import admin

from .models import *

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'dimension')
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'slug', 'description',
                    'duration', 'pub_date', 'image',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('ingredients', 'tags',)
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    empty_value_display = '-пусто-'
