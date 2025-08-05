
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name= "account"
urlpatterns = [
    path('login/', views.login_mobile, name='login'),
    path('login-password/', views.login_password, name='login-password'),
    path('verify-otp/', views.verify_otp, name='verify-otp'),
    path('logout/', views.logout_view, name='logout'),
    path('profile-edit/', views.profile_edit, name='profile-edit'),
    path('profile-dashboard/', views.profile_dashboard, name='profile-dashboard'),
    path('profile-address/', views.profile_address, name='profile-address'),
    path('profile/address/edit/<int:address_id>/', views.edit_address, name='edit-address'),
    path('address/delete/<int:pk>/', views.delete_address, name='delete_address'),
    path('profile-orders/', views.profile_orders, name='profile-orders'),
    path('profile-orders-detail/<int:order_id>/', views.profile_orders_detail, name='profile-orders-detail'),
    path('get_citys/', views.get_citys, name='get_citys'),

]
