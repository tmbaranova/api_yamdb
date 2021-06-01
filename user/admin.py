from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("pk", "email", "bio", "role", "first_name", "last_name")


admin.site.register(CustomUser, CustomUserAdmin)
