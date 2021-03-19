from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('my_cart', PurchasesViewSet, basename='my_cart')
# router.register('follow', FollowViewSet, basename='follow')
router.register('favorite', FavoritesViewSet, basename='favorite')
# router.register('ingredients', IngredientsView, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('ingredients/', IngredientsView.as_view(), name='ingredients-list'),
    path('follow/', post, name='follow_post'),
    path('follow/<int:id>', destroy, name='follow_delete'),
    # path('follow/', follow_post, name='follow_post'),
    # path('follow/<int:id>', follow_delete, name='follow_delete'),
]