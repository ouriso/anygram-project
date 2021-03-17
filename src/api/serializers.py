from django.db.models import fields
from rest_framework.generics import get_object_or_404
from recipes.models import Ingredient
from django.db import models
from rest_framework import serializers

from recipes.models import *

User = get_user_model()


# class FollowSerializer(serializers.Serializer):
#     id = serializers.PrimaryKeyRelatedField()

#     def validate_id(self, value):
#         user = get_object_or_404(User, pk=value)
#         if user:
#             return value


class CartSerializer(serializers.ModelSerializer):
    pass


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('pk', 'title', 'dimension')
