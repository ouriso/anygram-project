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


# class FollowViewSet(viewsets.ViewSet):
#     # Create, List, Destroy methods
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user

#     # @action(methods=['post'], detail=False)
#     def post(self, request):
#         user = self.get_object()
#         following_id = int(request.data.get('id', None))
#         if following_id is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         following = get_object_or_404(User, pk=following_id)
#         user.add(follow=following)
#         return Response(status.HTTP_201_CREATED)

#     # @action(methods=['destroy'], detail=True)
#     def destroy(self, request):
#         user = self.get_object()
#         following_id = int(self.kwargs.get('pk', None))
#         # following = get_object_or_404(User, pk=following_id)
#         user.follow.filter(pk=following_id).delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# follow_post = FollowViewSet.as_view({'post': 'post'})
# follow_delete = FollowViewSet.as_view({'delete': 'destroy'})
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post(request):
    user = request.user
    following_id = int(request.data.get('id', None))
    if following_id is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    following = get_object_or_404(User, pk=following_id)
    user.follow.add(following)
    return Response(status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def destroy(request, id):
    user = request.user
    # following_id = int(self.kwargs.get('pk', None))
    # following = get_object_or_404(User, pk=following_id)
    try:
        following = User.objects.get(pk=id)
        user.follow.remove(following)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # if user.follow.filter(pk=id).exists():
    #     user.follow.remove(pk=id)
    return Response(status=status.HTTP_204_NO_CONTENT)
    


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
