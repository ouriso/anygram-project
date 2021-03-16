from django import forms
from .models import Ingredient, Recipe, RecipeIngredient, Tag

class RecipeCreateForm(forms.ModelForm):
    # ingredients = forms.ModelMultipleChoiceField(RecipeIngredient)
    tags = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'duration', 'image', 'ingredients', 'tags')
