from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse
from .models import Product, Size, Order, OrderDetail, Category
from .cart import Cart
from account.models import Address
from django.http import JsonResponse

def store(request):
    products = Product.objects.all()
    for product in products:
        product.price = intcomma(product.price)
    return render(request,'store.html', {'products': products})

def categories(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if category is not None:
        products = Product.objects.filter(category__slug=category.slug)
        return render(request, 'category.html', {'category': category,
                                                 'products':products})


def product_detail(request, id:int):
    product = Product.objects.get(id=id)
    product.price = intcomma(product.price)
    # sizes = Size.objects.get(id=id)
    return render(request,'product-detail.html', {'product': product,
                                                  # 'sizes': sizes
                  })
@require_POST
def addtocart(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    product = Product.objects.get(id=product_id)
    update = True
    if request.POST.get('update')=='1':
        update = True
    else:
        update = False

    cart = Cart(request)
    cart.add(product_id, str(product.price),int(quantity),update)
    return redirect(reverse('tests:checkoutcart'))

def checkout_cart(request):
    return render(request,'checkout-cart.html')

def remove_from_cart(request, product_id):
    if Product.objects.filter(id=product_id).exists():
        cart = Cart(request)
        cart.remove(str(product_id))
        return redirect(reverse('tests:checkoutcart'))
    raise Http404('product not found')

def remove_all(request):
    cart = Cart(request)
    cart.clear()
    return redirect(reverse('tests:checkoutcart'))

def checkout_shipping(request):
    addresses = Address.objects.all().filter(user=request.user)
    cart = Cart(request)
    if request.method == 'POST':
        address_id = request.POST.get('address')
        if address_id:
            order = Order.objects.create(user=request.user,
                                         total_price= cart.get_totalprice,
                                         address_id=address_id)
            for item in cart:
                orderdetail = OrderDetail.objects.create(order = order,
                                                         product_id = item['product_id'],
                                                         quantity = item['quantity'],
                                                         price = item['price'])
            cart.clear()
            return redirect('tests:checkoutpayment')
        messages.error(request, "لطفا آدرس خود را انتخاب کنید")
    return render(request,'checkout-shipping.html', {'addresses': addresses})

def checkout_payment(request):
    return render(request,'checkout-payment.html')

@login_required
def add_address(request):
    if request.method == 'POST':
        address = Address.objects.create(
            user=request.user,
            recipient_firstname=request.POST.get('recipient_firstname'),
            recipient_lastname=request.POST.get('recipient_lastname'),
            recipient_phone=request.POST.get('recipient_phone'),
            city_id=request.POST.get('city'),
            postal_code=request.POST.get('postal_code'),
            number=request.POST.get('number'),
            unit=request.POST.get('unit'),
            address=request.POST.get('address'),
        )
        messages.success(request, "Address added successfully!")