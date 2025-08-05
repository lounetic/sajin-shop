
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name="shop"
urlpatterns = [
    path('', views.index, name='index'),
    path('live-search/', views.live_search, name='live-search'),
    path('update-cart/', views.update_cart_quantity, name='update_cart_quantity'),
]
