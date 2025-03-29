from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "full_name", "phone_number", "password1", "password2"]

    def clean_email(self):
        """Pastikan email unik"""
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email sudah digunakan.")
        return email

    def clean_phone_number(self):
        """Pastikan nomor telepon unik"""
        phone_number = self.cleaned_data.get("phone_number")
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Nomor telepon sudah digunakan.")
        return phone_number
