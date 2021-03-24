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

    title = models.CharField('название тега', max_length=30)
    slug = models.SlugField(unique=True)
    color = models.CharField(
        'выберите цвет тега',
        max_length=30, choices=Colors.choices, default=Colors.PURPLE
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Ingredient(models.Model):
    title = models.CharField('название ингредиента', max_length=50)
    slug = models.SlugField(unique=True)
    dimension = models.CharField('единицы измерения',
                                 max_length=15, default='шт.')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='автор рецепта')
    title = models.CharField('название рецепта', max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField('описание рецепта')
    duration = models.PositiveSmallIntegerField('время приготовления, мин')
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True,
                                    db_index=True)
    image = models.ImageField('изображение рецепта', upload_to='recipes/',
                              blank=True, null=True)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient', blank=True,
        verbose_name='ингредиенты для рецепта'
    )
    tags = models.ManyToManyField(
        Tag, related_name='recipes', blank=True,
        verbose_name='теги для рецепта'
    )
    in_favorite = models.ManyToManyField(
        User, related_name='favorites', blank=True,
        verbose_name='в избранном пользователей'
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('recipe', args=[str(self.slug)])


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField('количество для приготовления')

    class Meta:
        verbose_name = 'данные об ингредиенте'
        verbose_name_plural = 'данные об ингредиентах'
