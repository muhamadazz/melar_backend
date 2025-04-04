from django.db import models
from django.contrib.auth.models import User
from shops.models import Product
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s cart"


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancel_requested', 'Cancel Requested'),
        ('borrowed', 'Borrowed'),
        ('returning', 'Returning'),
        ('completed', 'Completed'),
    ]

    renter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='orders', null=True, blank=True
    )
    phone_renter = models.CharField(max_length=15, blank=True, null=True)

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='orders'
    )
    provider = models.CharField(max_length=255, blank=False, null=True)
    phone_provider = models.CharField(max_length=15, blank=False, null=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    borrow_date = models.DateField()
    return_deadline = models.DateField()
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.renter and not self.phone_renter:
            self.phone_renter = getattr(self.renter, 'phone_number', None)  # Gunakan getattr untuk menghindari error


        if not self.provider and self.product and self.product.shop and self.product.shop.user:
            self.provider = self.product.shop.user.full_name
            self.phone_provider = self.product.shop.user.phone_number

        super().save(*args, **kwargs)  # Simpan perubahan ke database


    def __str__(self):
        return f"Order #{self.id} - {self.renter.username if self.renter else 'Unknown'}"



class Shipping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping')
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    user_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Shipping for Order {self.order.id}"

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('shops.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x{self.quantity} in Order {self.order.id}"
