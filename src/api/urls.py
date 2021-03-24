from django.urls import path

from . import views

urlpatterns = [
    path('v1/ingredients/', views.IngredientsView.as_view(),
         name='ingredients-list'),
    path('v1/follow/', views.FollowView.as_view()),
    path('v1/follow/<int:id>/', views.FollowView.as_view()),
    path('v1/favorites/', views.FavoriteView.as_view()),
    path('v1/favorites/<int:id>/', views.FavoriteView.as_view()),
    path('v1/purchases/', views.PurchasesView.as_view()),
    path('v1/purchases/<int:id>/', views.PurchasesView.as_view()),
]
