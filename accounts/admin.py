from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from .models import Account
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm


class AccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
