from django.contrib import admin
from .models import MenuItem
from .forms import MenuItemForm


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemForm
    list_display = ['name', 'label', 'link', 'parent']
    list_filter = ['parent', 'name']
    search_fields = ['name', 'label']
