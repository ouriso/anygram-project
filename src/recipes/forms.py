from django import forms

from .models import Recipe, RecipeIngredient


class RecipeCreateForm(forms.ModelForm):
    title = forms.CharField(initial='Название рецепта')
    duration = forms.IntegerField(initial=30)
    description = forms.CharField(
        widget=forms.Textarea(), initial='Последовательность приготовления'
    )

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
