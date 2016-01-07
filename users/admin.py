from django.contrib import admin
from users.models import UserProfile, Address


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("owner", "street", "city", "state", "zip")