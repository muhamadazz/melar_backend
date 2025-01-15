from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Product, Category
from carts.models import Cart, CartItem
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError, PermissionDenied

User = get_user_model()

class CartTests(TestCase):
    def setUp(self):
        # Buat pengguna
        self.user = User.objects.create_user(username="testuser", email="testuser@gmail.com", password="password")
        
        # Buat kategori
        self.category = Category.objects.create(
            name="Test Category",
            description="A category for testing"
        )
        
        # Buat produk
        self.product = Product.objects.create(
            owner=self.user,
            name="Test Product",
            description="A test product",
            price=100.00,
            category=self.category,
        )
        
        # Buat keranjang untuk pengguna
        self.cart = Cart.objects.create(user=self.user)

        # Buat token JWT untuk pengguna
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_add_item_to_cart(self):
        """Test adding an item to the cart."""
        # Tambahkan produk ke keranjang melalui CartItem
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.cart, self.cart)
        self.assertEqual(cart_item.quantity, 2)

    def test_create_cart(self):
        """Test creating a new cart."""
        self.assertEqual(self.cart.user, self.user)

    def test_get_cart(self):
        """Test retrieving a cart."""
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart, self.cart)

    def test_cart_item_quantity_limit(self):
        """Test that the quantity of items in a cart is not negative."""
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        
        # Coba update quantity menjadi negatif
        cart_item.quantity = -1
        with self.assertRaises(ValidationError):
            cart_item.full_clean()  # Validasi manual
            cart_item.save()

    def test_cart_total_price(self):
        """Test the total price of the cart."""
        cart_item1 = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        cart_item2 = CartItem.objects.create(cart=self.cart, product=self.product, quantity=3)
        
        total_price = self.cart.get_total_price()
        expected_total_price = 2 * self.product.price + 3 * self.product.price
        self.assertEqual(total_price, expected_total_price)

    def test_empty_cart(self):
        """Test the behavior when the cart is empty."""
        empty_cart = Cart.objects.create(user=self.user)
        self.assertEqual(empty_cart.get_total_price(), 0.00)

    def test_authenticated_user_access(self):
        """Test that an authenticated user can access the cart."""
        # Akses API cart untuk pengguna yang sudah login dengan JWT
        response = self.client.get('/api/cart/', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)  # Pengguna terautentikasi harus dapat mengakses

    def test_unauthenticated_user_access(self):
        """Test that an unauthenticated user cannot access the cart."""
        # Akses API cart tanpa login (tanpa JWT)
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, 401)  # Harus meminta autentikasi

    def test_cart_item_create_for_another_user(self):
        """Test that one user cannot add items to another user's cart."""
        another_user = User.objects.create_user(username="anotheruser", email="anotheruser@gmail.com", password="password")
        cart_for_another_user = Cart.objects.create(user=another_user)
        
        # Simulasikan login untuk pengguna pertama
        self.client.login(username="testuser", password="password")

        # Kirim permintaan POST ke endpoint /api/cart-items/ dengan cart milik pengguna lain
        response = self.client.post(
            '/api/cart-items/',
            {'cart': cart_for_another_user.id, 'product': self.product.id, 'quantity': 1},
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'  # Token untuk user yang salah
        )

        # Pastikan mendapat status 403 Forbidden jika pengguna mencoba menambahkan item ke cart orang lain
        self.assertEqual(response.status_code, 403)
