from django import forms
from django.forms.models import BaseInlineFormSet

from .models import Ingredient, Recipe, RecipeIngredient


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


class MyIngredientFormSet(BaseInlineFormSet):

    def clean(self):
        ingredients = self.instance.recipeingredient_set.all()
        ing_from_form = []
        for form in self.forms:
            ingredient = form.cleaned_data.get('ingredient', None)
            if ingredient is None or \
                not Ingredient.objects.filter(title=ingredient).exists():
                form.cleaned_data['DELETE'] = True
                continue
            ing_from_form.append(ingredient.pk)
        if len(ing_from_form) != ingredients.count():
            i = RecipeIngredient.objects.filter(recipe=self.instance).exclude(ingredient__in=ing_from_form).delete()


IngredientFormSet = forms.inlineformset_factory(
    Recipe, RecipeIngredient, fields=('ingredient', 'amount'),
    formset=MyIngredientFormSet,
    form = RecipeIngredientForm
)



