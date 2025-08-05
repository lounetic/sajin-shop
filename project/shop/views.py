from django.contrib.humanize.templatetags.humanize import intcomma
from django.shortcuts import render
from tests.models import Category, Product
from tests.cart import Cart
from django.http import JsonResponse
from django.db.models import Q
import json
import random

# Create your views here.
def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    for product in products:
        product.price = intcomma(product.price)
        category_data = []

        for category in categories:
            cproducts = Product.objects.filter(category=category)
            random_image = None
            if cproducts.exists():
                random_product = random.choice(cproducts)
                random_image = random_product.main_image.url if random_product.main_image else None

            category_data.append({
                'category': category,
                'image': random_image,
            })
    return render(request,'index.html', {'products': products,'categories': categories,
                                         'category_data':category_data})

def live_search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        products = Product.objects.filter(
            Q(title__icontains=query)
        )[:10]  # Limit to 10 results

        results = [{'id': p.id, 'title': p.title,
                    'main_image': p.main_image.url if p.main_image else ''} for p in products]

    return JsonResponse({'results': results})

def update_cart_quantity(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    price = int(data.get('price'))
    action = data.get('action')

    cart = Cart(request)
    item = cart[product_id]

    current_quantity = item['quantity']
    if action == 'increment':
        cart.add(product_id, price, 1, update=False)
    elif action == 'decrement':
        if current_quantity > 1:
            cart.add(product_id, price, current_quantity - 1, update=True)
        else:
            cart.remove(product_id)

    updated = cart.cart.get(product_id)
    return JsonResponse({
        'quantity': updated['quantity'] if updated else 0,
        'total_price': f"{int(updated['quantity']) * int(updated['price']):,}" if updated else 0,
        'cart_total': f"{cart.get_totalprice:,}"
    })