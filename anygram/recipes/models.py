from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название тега', max_length=30)
    slug = models.SlugField(unique=True)


class Ingredient(models.Model):
    name = models.CharField('Название ингредиента', max_length=50)
    slug = models.SlugField(unique=True)
    dimension = models.CharField(max_length=15, default='шт.')


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Название рецепта', max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание рецепта')
    duration = models.TimeField('Время приготовления, мин')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True, db_index=True)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    tags = models.ManyToManyField('Теги для рецепта', Tag, related_name='recipes')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('-pub_date')


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()
