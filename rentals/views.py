from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Cart, Order, Shipping, Product
from .serializers import CartSerializer, OrderSerializer, ShippingSerializer
from .permissions import IsOrderOwnerOrReadOnly
from datetime import datetime
import logging
from .models import Order, OrderItem, Cart

logger = logging.getLogger(__name__)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Mengambil keranjang milik pengguna yang sedang login
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        user = self.request.user
        
        # Cek apakah produk sudah ada di keranjang pengguna
        existing_cart_item = Cart.objects.filter(user=user, product=product).first()
        
        if existing_cart_item:
            # Jika produk sudah ada, update quantity dan total_price
            logger.info(f"Existing cart item found: {existing_cart_item}")
            existing_cart_item.quantity += serializer.validated_data['quantity']
            existing_cart_item.total_price = existing_cart_item.product.price * existing_cart_item.quantity
            existing_cart_item.save()  # Simpan perubahan
        else:
            # Jika produk belum ada di keranjang, buat item baru
            logger.info(f"Creating new cart item for product {product.id}")
            serializer.save(user=user)  # Simpan item baru ke keranjang

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        borrow_date = request.data.get('borrow_date')
        return_deadline = request.data.get('return_deadline')

        # Ambil semua item di cart milik pengguna
        user_cart_items = Cart.objects.filter(user=request.user)

        if not user_cart_items:
            return Response({"detail": "Your cart is empty."}, status=400)

        if not borrow_date or not return_deadline:
            return Response({"detail": "Both borrow date and return deadline are required."}, status=400)

        try:
            borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d').date()
            return_deadline = datetime.strptime(return_deadline, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        if borrow_date >= return_deadline:
            return Response({"detail": "Return deadline must be after borrow date."}, status=400)

        # Hitung total harga berdasarkan item-item di Cart
        total_price = sum(item.product.price * item.quantity for item in user_cart_items)

        with transaction.atomic():
            # Membuat order baru
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                borrow_date=borrow_date,
                return_deadline=return_deadline,
            )

            # Menambahkan item-item Cart ke dalam OrderItem
            for cart_item in user_cart_items:
                # Membuat OrderItem untuk setiap Cart item
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    total_price=cart_item.total_price,
                )

            # Menghapus item Cart setelah berhasil checkout
            user_cart_items.delete()

        return Response({
            "detail": "Order created successfully",
            "order_id": order.id,
            "total_price": total_price
        }, status=status.HTTP_201_CREATED)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        # Menetapkan user ke dalam data serializer
        data = request.data
        data['user'] = request.user.id  # Menetapkan user yang sedang login

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()  # Menyimpan order
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def buy_now(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        borrow_date = request.data.get('borrow_date')
        return_deadline = request.data.get('return_deadline')

        # Validasi input
        if not product_id or not quantity or not borrow_date or not return_deadline:
            return Response({"detail": "Product, quantity, borrow_date, and return_deadline are required."}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=404)

        try:
            borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d').date()
            return_deadline = datetime.strptime(return_deadline, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        if borrow_date >= return_deadline:
            return Response({"detail": "Return deadline must be after borrow date."}, status=400)

        # Hitung total harga berdasarkan quantity
        total_price = product.price * quantity

        with transaction.atomic():
            # Membuat order baru
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                borrow_date=borrow_date,
                return_deadline=return_deadline,
            )

            # Membuat OrderItem untuk pembelian langsung
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                total_price=total_price
            )

        return Response({
            "detail": "Order created successfully",
            "order_id": order.id,
            "total_price": total_price
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def request_cancel(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response({"detail": "Cannot cancel order in current status"}, status=400)
        order.status = 'cancel_requested'
        order.save()
        return Response({"detail": "Cancel request submitted"}, status=200)

    @action(detail=True, methods=['post'])
    def confirm_received(self, request, pk=None):
        order = self.get_object()
        if order.status != 'shipping':
            return Response({"detail": "Order is not in shipping status"}, status=400)
        order.status = 'borrowed'
        order.save()
        return Response({"detail": "Order confirmed as borrowed"}, status=200)


class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [IsAuthenticated, IsOrderOwnerOrReadOnly]
