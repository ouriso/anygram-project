from django.urls import path

from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='index'),
    path('recipe/new/', views.RecipeCreateView.as_view(),
         name='recipe_new'),
    path('recipe/<slug:slug>/', views.RecipeSingleView.as_view(),
         name='recipe'),
    path('recipe/<slug:slug>/edit/', views.RecipeUpdateView.as_view(),
         name='recipe_edit'),
    path('recipe/author/<str:username>/',
         views.RecipeAuthorListView.as_view(), name='index_author'),
    path('follow/', views.FollowListView.as_view(), name='index_follow'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorites'),
]
