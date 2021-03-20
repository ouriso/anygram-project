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
