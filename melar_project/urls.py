"""
URL configuration for melar_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shops.viewset import *
from rentals.viewset import *
from django.contrib.auth.views import LoginView, LogoutView
from users.viewset import signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('shops.urls')), 
    path('api/', include('seller_requests.urls')),
    path('api/', include('rentals.urls')),
    path('', home, name='home'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('order/<int:product_id>/', create_order, name='create_order'),
    path('order/success/<int:order_id>/', order_success, name='order_success'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', signup, name='signup'),
]
