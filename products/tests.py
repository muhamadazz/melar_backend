from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from products.models import Category

class ProductAPITest(APITestCase):

    def setUp(self):
        # Buat pengguna 'seller' untuk tes
        self.seller_user = get_user_model().objects.create_user(
            email='seller@example.com',
            username='sellers123',
            password='securepassword',
            role='seller'  # Pastikan role adalah seller
        )
        
        # Buat pengguna 'customer' untuk tes akses kontrol
        self.customer_user = get_user_model().objects.create_user(
            email='customer@example.com',
            username='customer123',
            password='securepassword',
            role='user'  # Pastikan role adalah user
        )

        # Pastikan kategori dengan ID 1 ada di database
        self.category = Category.objects.create(name="Electronics")

        # Buat data produk untuk pengujian
        self.product_data = {
            'category': self.category.id,  # Gunakan ID kategori yang valid
            'name': 'Laptop',
            'description': 'Laptop gaming',
            'price': '500000.00',
            'owner': self.seller_user.id  # Pastikan owner adalah pengguna seller yang valid
        }

        # Buat client API dan login dengan token
        self.client = APIClient()
        self.client.force_authenticate(user=self.seller_user)

    def test_create_product(self):
        # Tes pembuatan produk baru
        response = self.client.post('/products/', self.product_data, format='json')
        print(response.data)  # Debug respons
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.product_data['name'])
        self.assertEqual(response.data['price'], self.product_data['price'])

    def test_create_product_invalid_category(self):
        # Menguji pembuatan produk dengan kategori yang tidak valid
        invalid_product_data = self.product_data.copy()
        invalid_product_data['category'] = 9999  # ID kategori yang tidak ada
        response = self.client.post('/products/', invalid_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('category', response.data)

    def test_create_product_without_authentication(self):
        # Tes pembuatan produk tanpa autentikasi (harus ditolak)
        self.client.force_authenticate(user=None)  # Logout user
        response = self.client.post('/products/', self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_product(self):
        # Buat produk terlebih dahulu
        response = self.client.post('/products/', self.product_data, format='json')
        product_id = response.data.get('id')  # Ambil ID produk dengan aman
        self.assertIsNotNone(product_id)  # Pastikan ID ada

        # Data yang akan diperbarui
        updated_data = {
            'name': 'Updated Laptop',
            'price': '600000.00',
            'category': self.category.id,  # Pastikan category ada
            'description': 'Updated Laptop gaming',  # Pastikan deskripsi ada
            'available': True,  # Pastikan available ada
            'owner': self.seller_user.id  # Pastikan owner ada
        }

        # Tes pembaruan produk
        response = self.client.put(f'/products/{product_id}/', updated_data, format='json')

        # Debug respons jika terjadi kesalahan
        print(response.data)  # Menampilkan error detail untuk debug

        # Periksa status respons dan data yang diperbarui
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])
        self.assertEqual(response.data['price'], updated_data['price'])
        self.assertEqual(response.data['description'], updated_data['description'])

    def test_update_product_without_permission(self):
        # Uji coba update produk oleh pengguna dengan role yang tidak berhak
        self.client.force_authenticate(user=self.customer_user)  # Login sebagai customer
        response = self.client.put('/products/1/', self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_product_list(self):
        # Buat produk terlebih dahulu
        response = self.client.post('/products/', self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Tes mendapatkan daftar produk
        response = self.client.get('/products/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Pastikan ada produk di daftar

    def test_get_product_detail(self):
        # Buat produk terlebih dahulu
        response = self.client.post('/products/', self.product_data, format='json')
        product_id = response.data.get('id')  # Ambil ID produk dengan aman
        self.assertIsNotNone(product_id)  # Pastikan ID ada

        # Tes mendapatkan detail produk
        response = self.client.get(f'/products/{product_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product_data['name'])
        self.assertEqual(response.data['price'], self.product_data['price'])

    def test_delete_product(self):
        # Buat produk terlebih dahulu
        response = self.client.post('/products/', self.product_data, format='json')
        product_id = response.data.get('id')  # Ambil ID produk dengan aman
        self.assertIsNotNone(product_id)  # Pastikan ID ada

        # Tes menghapus produk
        response = self.client.delete(f'/products/{product_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_without_permission(self):
        # Uji coba menghapus produk oleh pengguna yang tidak berhak
        self.client.force_authenticate(user=self.customer_user)  # Login sebagai customer
        response = self.client.delete('/products/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_nonexistent_product(self):
        # Menghapus produk yang tidak ada
        response = self.client.delete('/products/9999/', format='json')  # ID produk yang tidak ada
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
