from django import forms

from .models import Recipe, RecipeIngredient


class RecipeCreateForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'duration',
                  'image', 'ingredients', 'tags')


class RecipeIngredientForm(forms.ModelForm):
    title = forms.CharField()

    class Meta:
        model = RecipeIngredient
        fields = ('amount', 'title')


IngredientFormSet = forms.inlineformset_factory(
    Recipe, RecipeIngredient, fields=('ingredient', 'amount')
)
