from django.conf import settings
from recipes.models import Recipe


class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def in_cart(self, product_id):
        product_id = str(product_id)
        return product_id in self.cart

    def add(self, product_id):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product_id)
        if not self.in_cart(product_id):
            self.cart[product_id] = 1
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True
    
    def remove(self, product_id):
        """
        Удаление товара из корзины.
        """
        product_id = str(product_id)
        if self.in_cart(product_id):
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Recipe.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        # for item in self.cart.values():
        #     item['price'] = Decimal(item['price'])
        #     item['total_price'] = item['price'] * item['quantity']
        #     yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session['cart']
        self.session.modified = True
