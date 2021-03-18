from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import fields
from django.forms.models import BaseInlineFormSet
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import title
from .models import Ingredient, Recipe, RecipeIngredient, Tag

class RecipeCreateForm(forms.ModelForm):
    # ingredients = forms.ModelMultipleChoiceField(RecipeIngredient)
    # tags = forms.ModelMultipleChoiceField(
    #     widget=forms.CheckboxSelectMultiple,
    #     queryset=Tag.objects.all()
    # )

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'duration', 'image', 'ingredients', 'tags')


class RecipeIngredientForm(forms.ModelForm):
    title = forms.CharField()

    class Meta:
        model = RecipeIngredient
        fields = ('amount', 'title')


class MyIngredientFormSet(BaseInlineFormSet):

    def clean(self):
        for form in self.forms:
            ingredient_name = form.cleaned_data.get('title', None)
            if ingredient_name is None or \
                not Ingredient.objects.filter(title=ingredient_name).exists():
                form.cleaned_data['DELETE'] = True
                continue
            ingredient = Ingredient.objects.get(title=ingredient_name)
            form.cleaned_data['ingredient'] = ingredient.pk
            form.instance.ingredient = ingredient

IngredientFormSet = forms.inlineformset_factory(
    Recipe, RecipeIngredient, fields=('title', 'amount'),
    formset=MyIngredientFormSet,
    form = RecipeIngredientForm
)
