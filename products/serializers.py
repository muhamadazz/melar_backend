from rest_framework import serializers
from .models import Product, Category

# Serializer untuk Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Serializer untuk Product
class ProductSerializer(serializers.ModelSerializer):
    # Menggunakan PrimaryKeyRelatedField untuk relasi dengan Category
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = '__all__'
