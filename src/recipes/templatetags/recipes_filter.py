from urllib.parse import urlencode
from django import template
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
    d = context['request'].GET.copy()
    tag = kwargs.get('tag')
    page = kwargs.get('page')
    tags_context = d.getlist('tags', [])
    params = {}

    if page is not None:
        params['page'] = page

    if tag is not None:
        if str(tag) not in tags_context:
            tags_context.append(tag)
        else:
            tags_context.remove(tag)
        params['tags'] = tags_context
    elif tags_context != []:
        params['tags'] = tags_context

    return urlencode(params, doseq=True)
