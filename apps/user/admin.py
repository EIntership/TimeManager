from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Define a new user admin


# Re-register UserAdmin

admin.site.register(User, UserAdmin)