from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Address
# Register your models here.
admin.site.register(User, UserAdmin)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
  list_display = ('id','user_id','recipient_firstname', 'recipient_lastname', 'recipient_phone', 'postal_code')

