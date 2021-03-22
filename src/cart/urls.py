from .views import CartListView, delete_from_cart
from django.urls import path

urlpatterns = [
    path('', CartListView.as_view(), name='my_cart'),
    path('delete/<int:id>', delete_from_cart, name='delete_from_cart'),
]
