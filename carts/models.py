# carts/models.py
from django.db import models
from users.models import CustomUser  # Asumsi Anda memiliki model CustomUser
from products.models import Product  # Asumsi Anda memiliki model Product

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def get_total_price(self):
        total = sum(item.product.price * item.quantity for item in self.cart_items.all())
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"
