from django.urls import include, path

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('follow', views.FollowView, basename='follow')
router.register('favorites', views.FavoriteView, basename='favorites')
router.register('purchases', views.PurchasesView, basename='purchases')
router.register('ingredients', views.IngredientsView, basename='ingredients')

urlpatterns = [
    path('v1/', include(router.urls)),
]
