from recipes.models import Ingredient
from django.db import models
from rest_framework import serializers

from recipes.models import *


class CartSerializer(serializers.ModelSerializer):
    pass


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('pk', 'title', 'dimension')
