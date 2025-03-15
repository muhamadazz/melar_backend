from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import CartViewSet, OrderViewSet, ShippingViewSet

# Router untuk API utama
router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'shipping', ShippingViewSet, basename='shipping')

# Konfigurasi Swagger dan ReDoc
schema_view = get_schema_view(
    openapi.Info(
        title="E-Commerce Rentals API",
        default_version='v1',
        description="Dokumentasi API untuk layanan e-commerce rentals",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),  # Endpoint API utama
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
