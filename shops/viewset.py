from shops.models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Shop, Category
from .forms import ShopForm, ProductForm
from django.contrib import messages


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def user_shops(request):
    shops = request.user.shops.all()  # Ambil semua toko milik user
    return render(request, 'shops/user_shops.html', {'shops': shops})

@login_required
def shop_products(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id, user=request.user) 
    products = shop.products.all()
    return render(request, 'shops/shop_products.html', {'shop': shop, 'products': products})

@login_required
def add_shop(request):
    if request.method == "POST":
        form = ShopForm(request.POST)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.user = request.user  # Gunakan user sesuai field di model
            shop.save()
            return redirect('user_shops')
    else:
        form = ShopForm()
    
    return render(request, 'shops/add_shop.html', {'form': form})

@login_required
def shop_detail(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id, user=request.user)
    return render(request, 'shops/shop_detail.html', {'shop': shop})


@login_required
def delete_shop(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)
    if request.method == "POST":
        shop.delete()
        return redirect('user_shops')

    return render(request, 'shops/delete_shop.html', {'shop': shop})

@login_required
def edit_shop(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id, user=request.user)
    
    if request.method == "POST":
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('user_shops')
    else:
        form = ShopForm(instance=shop)
    
    return render(request, 'shops/edit_shop.html', {'form': form, 'shop': shop})


@login_required
def add_product(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id, user=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.save()

            # Tambahkan kategori baru jika diisi
            new_category_name = form.cleaned_data.get('new_category')
            if new_category_name:
                category, created = Category.objects.get_or_create(name=new_category_name)
                product.categories.add(category)  # Hubungkan kategori ke produk

            form.save_m2m()  # Simpan kategori ManyToMany
            return redirect('shop_products', shop_id=shop.id)
    else:
        form = ProductForm()

    return render(request, 'shops/add_product.html', {'form': form, 'shop': shop})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, shop__user=request.user)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop_products', shop_id=product.shop.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'shops/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, shop__user=request.user)
    shop_id = product.shop.id
    
    if request.method == "POST":
        product.delete()
        return redirect('shop_products', shop_id=shop_id)

    return render(request, 'shops/delete_product.html', {'product': product})

