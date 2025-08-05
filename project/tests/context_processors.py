from decimal import Decimal

from .cart import Cart
from .models import Product, Category

def cart(request):
    cart_session = Cart(request)
    if cart_session:
        product_ids = cart_session.product_ids
        products = Product.objects.filter(id__in=product_ids)
        for item in products:
            cart_session[str(item.id)]['product'] = item
        all_total_price = 0
        cart_length = 0
        product_length = 0
        for item in cart_session:
            item['totalprice'] = int(item['price']) * item['quantity']
            all_total_price += item['totalprice']
            cart_length += item['quantity']
            product_length += 1

        cart_session.all_total_price = all_total_price
        cart_session.cart_length = cart_length
        cart_session.product_length = product_length

        return {'cart':cart_session,
                'product_length':product_length,
                'categories': Category.objects.all()}
