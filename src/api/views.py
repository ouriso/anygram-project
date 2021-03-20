from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from recipes.models import Ingredient, Recipe
from cart.cart import Cart

from .serializers import CartSerializer, IngredientSerializer

User = get_user_model()


SUCCESS = {"success": True}
UNSUCCESS = {"success": False}


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


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_post(request):
    user = request.user
    following_id = int(request.data.get('id', None))
    if following_id is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    following = get_object_or_404(User, pk=following_id)
    user.follow.add(following)
    return Response(status=status.HTTP_201_CREATED, data=SUCCESS)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def follow_destroy(request, id):
    user = request.user
    try:
        following = User.objects.get(pk=id)
        user.follow.remove(following)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=UNSUCCESS)
    return Response(status=status.HTTP_202_ACCEPTED, data=SUCCESS)
    
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def favorite_post(request):
    user = request.user
    recipe_id = int(request.data.get('id', None))
    if recipe_id is None:
        return Response(status=status.HTTP_404_NOT_FOUND, data=UNSUCCESS)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.in_favorite.add(user)
    return Response(status=status.HTTP_201_CREATED, data=SUCCESS)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def favorite_destroy(request, id):
    user = request.user
    try:
        recipe = Recipe.objects.get(pk=id)
        recipe.in_favorite.remove(user)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=UNSUCCESS)
    return Response(status=status.HTTP_202_ACCEPTED, data=SUCCESS)


class IngredientsView(ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'slug']
