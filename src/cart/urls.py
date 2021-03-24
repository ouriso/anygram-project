from django.urls import path

from .views import CartListView, delete_from_cart, download_cart

urlpatterns = [
    path('', CartListView.as_view(), name='my_cart'),
    path('delete/<int:id>/', delete_from_cart, name='delete_from_cart'),
    path('download/', download_cart, name='cart_download'),
]
