from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, phone_number, password=None, **extra_fields):
        """Buat pengguna biasa dengan email, username, dan phone_number."""
        if not email:
            raise ValueError('Email harus diisi')
        if not phone_number:
            raise ValueError('Nomor telepon harus diisi')

        email = self.normalize_email(email)
        extra_fields.setdefault('role', 'user')

        user = self.model(email=email, username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number, password=None, **extra_fields):
        """Buat superuser dengan akses staff dan superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser harus memiliki is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser harus memiliki is_superuser=True.')

        return self.create_user(email, username, phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),  # Role user untuk pengguna biasa, yang dapat menjadi customer atau seller
    )

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)  # ✅ Nomor telepon wajib diisi dan unik
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')
    is_seller = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'phone_number']  # ✅ Tambahkan phone_number sebagai field wajib

    def __str__(self):
        role_display = "Admin" if self.role == 'admin' else "Seller" if self.is_seller else "Customer"
        return f"{self.email} ({role_display})"
