from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from recipes.forms import IngredientFormSet, RecipeCreateForm

from .models import Recipe, RecipeIngredient
from .utils import filter_by_tags

User = get_user_model()


class RecipeListView(ListView):
    paginate_by = 9
    template_name = 'recipes/recipe_index.html'

    def get_queryset(self):
        queryset = Recipe.objects.all()
        queryset, self.filter_tags = filter_by_tags(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все рецепты Anygram'
        context['tags'] = self.filter_tags
        return context


class RecipeAuthorListView(ListView):
    paginate_by = 9
    template_name = 'recipes/recipe_author.html'

    def get_author(self):
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        return author

    def get_queryset(self):
        queryset = Recipe.objects.filter(author=self.get_author())
        queryset, self.filter_tags = filter_by_tags(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        author = self.get_author()
        context = super().get_context_data(**kwargs)
        context['title'] = f'Рецепты автора {author.first_name}'
        context['id'] = author.pk
        context['tags'] = self.filter_tags
        return context


class RecipeSingleView(DetailView):
    queryset = Recipe.objects.all()
    template_name = 'recipes/recipe_single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipeingredients'] = RecipeIngredient.objects.filter(
            recipe=self.get_object()
        )
        context['tags'] = self.get_object().tags.all()
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeCreateForm
    template_name = 'recipes/recipe_form.html'
    success_url = ''

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredient_form = IngredientFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredient_form=ingredient_form)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredient_form = IngredientFormSet(self.request.POST)
        if (form.is_valid() and ingredient_form.is_valid()):
            return self.form_valid(form, ingredient_form)
        else:
            return self.form_invalid(form, ingredient_form)

    def form_valid(self, form, ingredient_form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        ingredient_form.instance = self.object
        ingredient_form.instance.tags.set(form.cleaned_data.get('tags'))
        ingredient_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ingredient_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredient_form=ingredient_form))


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeCreateForm
    template_name = 'recipes/recipe_form.html'
    success_url = ''

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            return HttpResponseForbidden()
        form = RecipeCreateForm(instance=self.object)
        ingredient_form = IngredientFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredient_form=ingredient_form,
                                  recipe=self.object))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = RecipeCreateForm(
            self.request.POST, self.request.FILES, instance=self.object
        )
        ingredient_form = IngredientFormSet(
            self.request.POST, instance=self.object
        )
        if (form.is_valid() and ingredient_form.is_valid()):
            return self.form_valid(form, ingredient_form)
        else:
            return self.form_invalid(form, ingredient_form)

    def form_valid(self, form, ingredient_form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        ingredient_form.instance = self.object
        ingredient_form.instance.tags.set(form.cleaned_data.get('tags'))
        ingredient_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ingredient_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredient_form=ingredient_form))


class FavoriteListView(LoginRequiredMixin, ListView):
    paginate_by = 9
    template_name = 'recipes/recipe_index.html'

    def get_queryset(self):
        queryset = Recipe.objects.filter(in_favorite=self.request.user)
        queryset, self.filter_tags = filter_by_tags(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Избранные рецепты'
        context['tags'] = self.filter_tags
        return context


class FollowListView(LoginRequiredMixin, ListView):
    paginate_by = 3
    template_name = 'recipes/follow_index.html'

    def get_queryset(self):
        queryset = list(self.request.user.follow.all())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваши подписки'
        return context
