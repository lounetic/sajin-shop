from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Category, Size, Order, OrderDetail
from django.urls import reverse
# Register your models here.

class OrderDetailInline(admin.TabularInline):  # or admin.StackedInline for vertical layout
  model = OrderDetail
  extra = 0  # no extra empty forms
  readonly_fields = ['product', 'quantity', 'price']  # optional: make read-only
  can_delete = False  # optional: disallow deleting items from here

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ['id', 'user_link', 'total_price', 'status']
  def user_link(self, obj):
      if obj.user:
          url = reverse('admin:account_user_change', args=[obj.user.id])
          return format_html('<a href="{}">{}</a>', url, obj.user.get_full_name() or obj.user.username)
      return '-'
  user_link.short_description = 'User'
  list_filter = ['status']
  search_fields = ['id', 'user__email']
  inlines = [OrderDetailInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['id', 'title', 'slug']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ['id', 'title', 'price', 'category__title', 'quantity']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
  list_display = ("size",  )