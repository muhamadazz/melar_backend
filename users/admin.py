from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):  # Gunakan UserAdmin agar sesuai dengan Django
    list_display = ('email', 'username', 'full_name', 'role', 'is_seller', 'is_active', 'is_staff', 'created_at')
    list_filter = ('role', 'is_seller', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'full_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Roles and Permissions', {'fields': ('role', 'is_seller', 'is_active', 'is_staff', 'is_superuser')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),  
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'full_name', 'role', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        """Pastikan password di-hash jika dibuat atau diperbarui dari admin"""
        if change:  # Jika sedang mengedit user
            if 'password' in form.cleaned_data and form.cleaned_data['password']:
                obj.set_password(form.cleaned_data['password'])
        else:  # Jika user baru dibuat
            obj.set_password(obj.password)

        super().save_model(request, obj, form, change)
