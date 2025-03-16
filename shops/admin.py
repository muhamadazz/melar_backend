from django.contrib import admin
from .models import Shop, Category, Product, Discount, Inventory

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user', 'is_active', 'address', 'contact', 'created_at')
    search_fields = ('shop_name', 'user__username', 'address')
    list_filter = ('is_active',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'get_owner', 'price', 'availability_status', 'status', 'created_at')
    search_fields = ('name', 'shop__shop_name', 'shop__user__username')
    list_filter = ('availability_status', 'status', 'categories')
    ordering = ('-created_at',)

    def get_owner(self, obj):
        return obj.shop.user.username  # Mengambil username pemilik toko
    get_owner.short_description = "Owner"  # Nama kolom di Django Admin

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'percentage', 'valid_from', 'valid_until', 'admin', 'product', 'category')
    search_fields = ('code', 'admin__username')
    list_filter = ('valid_from', 'valid_until')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'created_at')
    search_fields = ('product__name',)
