from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from pytils.translit import slugify

User = get_user_model()


class Tag(models.Model):
    class Colors(models.TextChoices):
        ORANGE = 'badge badge_style_orange'
        GREEN = 'badge badge_style_green'
        PURPLE = 'badge badge_style_purple'

    title = models.CharField('Название тега', max_length=30)
    slug = models.SlugField(unique=True)
    color = models.CharField(
        'Выберите цвет тега',
        max_length=30, choices=Colors.choices, default=Colors.PURPLE
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField('Название ингредиента', max_length=50)
    slug = models.SlugField(unique=True)
    dimension = models.CharField(max_length=15, default='шт.')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField('Название рецепта', max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание рецепта')
    duration = models.PositiveSmallIntegerField('Время приготовления, мин')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True, db_index=True)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', blank=True)
    tags = models.ManyToManyField(Tag, related_name='recipes', blank=True)
    in_favorite = models.ManyToManyField(User, related_name='favorites', blank=True)

    def get_absolute_url(self):
        return reverse('recipe', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('-pub_date',)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()
