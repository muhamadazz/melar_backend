from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter keranjang berdasarkan pengguna yang terautentikasi
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Membuat cart baru untuk pengguna jika belum ada
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart = serializer.validated_data.get('cart')

        # Pastikan cart ada dan hanya pengguna yang memiliki cart yang bisa menambahkan item
        if not cart:
            raise PermissionDenied("Cart not provided or invalid.")
        
        if cart.user != self.request.user:
            raise PermissionDenied("You cannot add items to another user's cart.")

        serializer.save()
