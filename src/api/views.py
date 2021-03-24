from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart
from recipes.models import Ingredient, Recipe

from .serializers import IngredientSerializer

User = get_user_model()


SUCCESS = {"success": True}
UNSUCCESS = {"success": False}


class AddMixin:
    model = None

    def get_instance(self, request):
        id = request.data.get('id')
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
        following = get_object_or_404(User, pk=id)
        user.follow.remove(following)
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
        recipe = get_object_or_404(Recipe, pk=id)
        recipe.in_favorite.remove(user)
        return Response(status=status.HTTP_202_ACCEPTED, data=SUCCESS)


class PurchasesView(APIView):

    def post(self, request):
        id = request.data.get('id')
        cart = Cart(self.request)
        if not Recipe.objects.filter(pk=id).exists() or cart.in_cart(id):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=UNSUCCESS)
        cart.add(id)
        return Response(status=status.HTTP_201_CREATED, data=SUCCESS)

    def delete(self, request, id):
        cart = Cart(request)
        if Recipe.objects.filter(pk=id).exists() and cart.in_cart(id):
            cart.remove(id)
            return Response(status=status.HTTP_202_ACCEPTED, data=SUCCESS)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=UNSUCCESS)


class IngredientsView(ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'slug']
