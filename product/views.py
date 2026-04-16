from django.shortcuts import render, redirect

from product.forms import ProductForm
from product.models import Product


# Create your views here.
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/list.html', {'products': products})


def product_create(request):
    form = ProductForm()
    return render(request, 'product/create.html', {'form': form})


def product_create_save(request):
    form = ProductForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'product/create.html', {'form': form})


def product_update_form(request, pk=None):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    return render(request, 'product/update.html', {'form': form, 'p': product})


def product_update(request, pk=None):
    product = Product.objects.get(id=pk)
    form = ProductForm(request.POST, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'product/update.html', {'form': form, 'p': product})
