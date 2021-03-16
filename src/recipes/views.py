from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import models
from django.http import request, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.urls.base import reverse

from recipes.forms import RecipeCreateForm
from .models import Recipe, RecipeIngredient
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, ListView


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


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeCreateForm
    template_name = 'recipe_create.html'
    success_url = ''

    # def get(self, request, *args, **kwargs):
    #     self.object = None
    #     form = self.get_form(self.get_form_class())
    #     return self.render_to_response(
    #         self.get_context_data(form=form)
    #     )

    # def post(self, request, *args, **kwargs):
    #     self.object = None
    #     form = self.get_form(self.get_form_class())
    #     print(form)
    #     form = form(self.request.POST)
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    def form_valid(self, form):
        # print(form.cleaned_data)
        print(self.request.POST.getlist('entries'))
        self.object = form.save(commit=False)
        # print(self.object)
        # title = form.cleaned_data['title']
        # slug = slugify(title)
        # print(title, slug)
        # form.save(commit=False)
        form.instance.author = self.request.user
        # form.instance.slug = slug
        # self.object.save()
        return super().form_valid(form)

    # def form_invalid(self, form):
    #     return self.render_to_response(
    #         self.get_context_data(form=form)
    #     )


    # def get(self, request, *args, **kwargs):
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     ingredient_form = IngredientFormSet()
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               ingredient_form=ingredient_form)
    #     )

    # def post(self, request, *args, **kwargs):
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     print(form)
    #     ingredient_form = IngredientFormSet(self.request.POST)
    #     if (form.is_valid() and ingredient_form.is_valid()):
    #         return self.form_valid(form, ingredient_form)
    #     else:
    #         return self.form_invalid(form, ingredient_form)

    # def form_valid(self, form, ingredient_form):
    #     self.object = form.save(commit=False)
    #     self.author = self.request.user
    #     self.object.save()
    #     ingredient_form.instance = self.object
    #     ingredient_form.save()
    #     return HttpResponseRedirect(self.get_success_url())

    # def form_invalid(self, form, ingredient_form):
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               ingredient_form=ingredient_form))
