from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Ingredient, Recipe
from cart.cart import Cart

from .serializers import CartSerializer, IngredientSerializer

User = get_user_model()


SUCCESS = {"success": True}
UNSUCCESS = {"success": False}


class AddMixin:
    model = None

    def get_instance(self, request):
        user = request.user
        id = int(request.data.get('id', None))
        if id is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instance = get_object_or_404(self.model, pk=id)
        return instance


class FollowView(AddMixin, APIView):
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        instance = self.get_instance(request)
        request.user.follow.add(instance)
        return Response(status=status.HTTP_201_CREATED, data=SUCCESS)

    def delete(self, request, id):
        user = request.user
        try:
            following = User.objects.get(pk=id)
            user.follow.remove(following)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=UNSUCCESS)
        return Response(status=status.HTTP_202_ACCEPTED, data=SUCCESS)


class FavoriteView(AddMixin, APIView):
    model = Recipe
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        recipe = self.get_instance(request)
        recipe.in_favorite.add(request.user)
        return Response(status=status.HTTP_201_CREATED, data=SUCCESS)

    def delete(self, request, id):
        user = request.user
        try:
            recipe = Recipe.objects.get(pk=id)
            recipe.in_favorite.remove(user)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=UNSUCCESS)
        return Response(status=status.HTTP_202_ACCEPTED, data=SUCCESS)


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
        return Response(status=status.HTTP_201_CREATED, data=SUCCESS)


class IngredientsView(ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'slug']
