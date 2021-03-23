from django.urls import path

from . import views

urlpatterns = [
    path('ingredients/', views.IngredientsView.as_view(),
         name='ingredients-list'),
    path('follow/', views.FollowView.as_view()),
    path('follow/<int:id>/', views.FollowView.as_view()),
    path('favorites/', views.FavoriteView.as_view()),
    path('favorites/<int:id>/', views.FavoriteView.as_view()),
    path('purchases/', views.PurchasesView.as_view()),
    path('purchases/<int:id>/', views.PurchasesView.as_view()),
]
