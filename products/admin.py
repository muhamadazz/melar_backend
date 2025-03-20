from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'price', 'category', 'available', 'created_at')
    search_fields = ('name', 'owner__username', 'category__name')
    list_filter = ('available', 'category', 'owner')
    ordering = ('-created_at',)
