from django.conf import settings


class Cart():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def in_cart(self, product_id):
        product_id = str(product_id)
        return product_id in self.cart

    def add(self, product_id):
        """
        Добавить продукт в корзину или обновить его количество
        """
        product_id = str(product_id)
        if not self.in_cart(product_id):
            self.cart[product_id] = 1
        self.save()

    def save(self):
        """
        Обновление сессии cart
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product_id):
        """
        Удаление товара из корзины
        """
        product_id = str(product_id)
        if self.in_cart(product_id):
            del self.cart[product_id]
            self.save()

    def get_ids(self):
        """
        Получение всех элементов корзины
        """
        return self.cart.keys()

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return len(self.cart)

    def clear(self):
        """
        Удаление корзины из сессии
        """
        del self.session['cart']
        self.session.modified = True
