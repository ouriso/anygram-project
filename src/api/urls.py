from django.urls import include, path

from .views import *

urlpatterns = [
    path('ingredients/', IngredientsView.as_view(), name='ingredients-list'),
    path('follow/', FollowView.as_view()),
    path('follow/<int:id>/', FollowView.as_view()),
    path('favorites/', FavoriteView.as_view()),
    path('favorites/<int:id>/', FavoriteView.as_view()),
]
