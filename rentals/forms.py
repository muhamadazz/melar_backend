from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['borrow_date', 'return_deadline', 'total_price']
        widgets = {
            'borrow_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'return_deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'total_price': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        borrow_date = cleaned_data.get("borrow_date")
        return_deadline = cleaned_data.get("return_deadline")

        if borrow_date and return_deadline and return_deadline <= borrow_date:
            raise forms.ValidationError("Tanggal kembali harus lebih besar dari tanggal sewa!")
        
        return cleaned_data
