import io

import reportlab
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import redirect
from django.views.generic import ListView
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from cart.cart import Cart
from recipes.models import Recipe, RecipeIngredient


class CartListView(ListView):
    template_name = 'cart/my_cart.html'

    def get_queryset(self):
        cart = Cart(self.request)
        recipes_id = cart.get_ids()
        return Recipe.objects.filter(pk__in=recipes_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список покупок'
        return context


def delete_from_cart(request, id):
    cart = Cart(request)
    if cart.in_cart(id):
        cart.remove(id)
    return redirect('my_cart')


def prepare_file(string_list):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    reportlab.rl_config.TTFSearchPath.append(str(settings.BASE_DIR) + '/cart')
    pdfmetrics.registerFont(TTFont('Cyril', 'CYRIL1.TTF'))
    p.setFont('Cyril', 14)
    x = 50
    y = 800
    for line in string_list:
        p.drawString(x, y, line)
        y -= 20
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer


def download_cart(request):
    cart = Cart(request)
    recipes_id = cart.get_ids()
    recipes = RecipeIngredient.objects.filter(
        recipe__pk__in=recipes_id
    ).select_related('ingredient').select_related('recipe')
    recipe_names = set()
    ingredients_count = {}
    for item in recipes:
        recipe_names.add(item.recipe.title)

        title = item.ingredient.title
        amount = item.amount
        dimension = item.ingredient.dimension
        ing = ingredients_count.get(title, [0, dimension])
        ingredients_count[title] = [ing[0] + amount, dimension]

    to_file = ['Список покупок\n', 'Для рецептов:\n']
    for title in recipe_names:
        to_file.append(title+'\n')
    to_file.append('\nКупить следующее:\n')
    for k, v in ingredients_count.items():
        to_file.append(f'- {k}: {v[0]} {v[1]}\n')

    file = prepare_file(to_file)
    return FileResponse(file, as_attachment=True, filename='cart.pdf')
