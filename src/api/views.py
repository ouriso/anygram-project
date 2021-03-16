from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from recipes.models import Ingredient, Recipe
from cart.cart import Cart

from .serializers import CartSerializer, IngredientSerializer


class PurchasesViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    # Create, List, Destroy methods
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart = Cart(self.request)
        product_ids = cart.cart.keys()
        # получение объектов product и добавление их в корзину
        return Recipe.objects.filter(pk__in=product_ids)

    def perform_create(self, serializer):
        cart = Cart(self.request)
        recipe = get_object_or_404(Recipe, pk=serializer.data['id'])
        cart.add(recipe)
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        cart = Cart(self.request)
        recipe = get_object_or_404(Recipe, pk=kwargs['id'])
        cart.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    # Create, List, Destroy methods
    pass


class FavoritesViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    # Create, List, Destroy methods
    pass


class IngredientsView(ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'slug']
