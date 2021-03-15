from django.contrib.auth import get_user_model
from .models import Recipe, RecipeIngredient
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView


User = get_user_model()


class RecipeListView(ListView):
    queryset = Recipe.objects.all()
    paginate_by = 9
    template_name = 'recipe_index.html'


class RecipeAuthorListView(ListView):
    paginate_by = 9
    template_name = 'recipe_author.html'

    def get_author(self):
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        return author

    def get_queryset(self):
        queryset = Recipe.objects.filter(author=self.get_author())
        return queryset

    def get_context_data(self, **kwargs):
        author = self.get_author()
        context = super().get_context_data(**kwargs)
        context['title'] = f'Рецепты автора {author.first_name}'
        return context


class RecipeSingleView(DetailView):
    queryset = Recipe.objects.all()
    template_name = 'recipe_single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipeingredients'] = RecipeIngredient.objects.filter(recipe=self.get_object())
        return context
