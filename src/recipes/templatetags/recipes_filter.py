from urllib.parse import urlencode

from django import template

from cart.cart import Cart

register = template.Library()


@register.simple_tag
def is_favorite(recipe, user):
    return user.favorites.all().filter(pk=recipe.pk).exists()


@register.simple_tag
def is_following(user, author_id):
    return user.follow.all().filter(pk=author_id).exists()


@register.simple_tag
def get_recipes(author):
    recipes = author.recipes.all()
    return recipes[:3]


@register.simple_tag
def recipes_count(recipes):
    return recipes.count() - 3


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    cur_params = context['request'].GET.copy()
    tag = kwargs.get('tag')
    page = kwargs.get('page')
    tags_context = cur_params.getlist('tags', [])
    new_params = {}

    if page is not None:
        new_params['page'] = page

    if tag is not None:
        if str(tag) not in tags_context:
            tags_context.append(tag)
        else:
            tags_context.remove(tag)
        new_params['tags'] = tags_context
    elif tags_context != []:
        new_params['tags'] = tags_context

    return urlencode(new_params, doseq=True)


@register.simple_tag(takes_context=True)
def recipe_in_cart(context, id):
    cart = Cart(context['request'])
    return cart.in_cart(id)
