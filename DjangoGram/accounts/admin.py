from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserManager


admin.site.register(User)
