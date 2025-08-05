from decimal import Decimal

cart_session_id = 'cart'
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(cart_session_id)
        if not cart:
            cart = self.session[cart_session_id] = {}
        self.cart = cart

    def __getitem__(self, item):
        return self.cart[item]

    def add(self, product_id, price, quantity, update):
        if product_id not in self.cart:
            self.cart[product_id] = {
                'product_id': product_id,
                'quantity': 0,
                'price': price,
            }
        if update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.session[cart_session_id] = self.cart
        self.session.modified = True

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
        self.session[cart_session_id] = self.cart
        self.session.modified = True

    def clear(self): #خالی کردن سبد خرید بعد از چک اوت
        self.session[cart_session_id] = {}
        self.session.modified = True

    @property
    def product_ids(self):
        return self.cart.keys()

    @property
    def get_totalprice(self):
        all_total_price = 0
        for item in self.cart.values():
            item['totalprice'] = int(item['price']) * item['quantity']
            all_total_price += item['totalprice']
        return all_total_price


    def __iter__(self):
        for item in self.cart.values():
            yield item