from .views import *
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    # Список рецептов, начальная страница
    path('', RecipeListView.as_view(), name='index'),
    # Создание рецепта
    path('recipe/new/', RecipeCreateView.as_view(), name='recipe_new'),
    # Страница с рецептом
    path('recipe/<slug:slug>/', RecipeSingleView.as_view(), name='recipe'),
    # Редактирование рецепта
    path('recipe/<slug:slug>/edit/', RecipeUpdateView.as_view(), name='recipe_edit'),
    # Список рецептов автора
    path('recipe/author/<str:username>/', RecipeAuthorListView.as_view(), name='index_author'),
    # Список рецептов по подписке
    # Список избранных рецептов
    path('favorites/', FavoriteListView.as_view(), name='favorites'),


    # path('/', views.as_view(), name='index'),
    # path('author/', ),
    # path('recipes/', ),
    # path('')
]