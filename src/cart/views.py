from django.shortcuts import redirect
from django.views.generic import ListView
from cart.cart import Cart

from recipes.models import Recipe

# Create your views here.

class CartListView(ListView):
    template_name = 'my_cart.html'

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
