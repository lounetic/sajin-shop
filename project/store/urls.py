
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name='store'
urlpatterns = [
    path('store/', views.store, name='store'),
    path('store/<int:id>', views.product_detail, name='productdetail'),
    path('category/<slug:slug>/', views.categories, name='category_store'),
    path('checkoutcart/', views.checkout_cart, name='checkoutcart'),
    path('checkoutshipping/', views.checkout_shipping, name='checkoutshipping'),
    path('checkoutpayment/', views.checkout_payment, name='checkoutpayment'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('add_address/', views.add_address, name='add_address'),
    path('removefromcart/<int:product_id>', views.remove_from_cart, name='removefromcart'),
    path('remove-all/', views.remove_all, name='remove-all'),
]
