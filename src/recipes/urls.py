from .views import *
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    # Список рецептов, начальная страница
    path('', RecipeListView.as_view(), name='index'),
    # Страница с рецептом
    path('recipe/<slug:slug>', RecipeSingleView.as_view(), name='recipe'),
    # Список рецептов автора
    path('recipe/author/<str:username>', RecipeAuthorListView.as_view(), name='index_author'),
    # Список рецептов по подписке
    # Список избранных рецептов
    # Создание рецепта
    # Редактирование рецепта

    # path('/', views.as_view(), name='index'),
    # path('author/', ),
    # path('recipes/', ),
    # path('')
]