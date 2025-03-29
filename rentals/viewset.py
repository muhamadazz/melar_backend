from datetime import datetime
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order  # Pastikan model produk ada
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.conf import settings

@login_required(login_url=settings.LOGIN_URL)
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.renter = request.user  # Sesuai user yang login

            # Ambil data dari form
            borrow_date = form.cleaned_data["borrow_date"]
            return_deadline = form.cleaned_data["return_deadline"]
            quantity = int(request.POST.get("quantity", 1))

            # Hitung total harga
            if borrow_date and return_deadline:
                days = (return_deadline - borrow_date).days
                days = max(days, 1)  # Jika hanya 1 hari tetap dihitung 1 hari
                total_price = product.price * quantity * days
            else:
                total_price = product.price * quantity  # Default jika tanpa tanggal

            order.total_price = total_price  # Simpan total harga ke database
            order.save()
            return redirect('order_success', order_id=order.id)  # Redirect ke halaman sukses

    else:
        form = OrderForm()

    return render(request, 'order_form.html', {'form': form, 'product': product})



def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})

