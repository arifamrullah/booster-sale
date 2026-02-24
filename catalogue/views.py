import re

from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models.category import Category
from .models.product import Product
from .models.product_image import ProductImage
from .models.color import Color
from .models.size import Size
from .models.product_variant import ProductVariant
from .forms import ProductForm, ProductVariantForm, ProductVariantFormSet

def parse_variants(post_data):
    variants = {}
    pattern = re.compile(r'^variants\[(\d+)\]\[(\w+)\]$')

    for key, value in post_data.items():
        match = pattern.match(key)
        if match:
            index, field = match.groups()
            variants.setdefault(index, {})[field] = value

    return list(variants.values())

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products' : products})

def product_create(request):
    sizes = Size.objects.all()
    colors = Color.objects.all()

    if request.method == 'POST':
        product_form = ProductForm(request.POST)

        if product_form.is_valid():
            product = product_form.save()

            if product.has_variant:
                variants = parse_variants(request.POST)

                for v in variants:
                    raw = v.get('is_active')

                    ProductVariant.objects.create(
                        product=product,
                        color_id=v['color_id'],
                        size_id=v['size_id'],
                        sku=v['sku'],
                        price=v['price'],
                        stock=v['stock'],
                        weight=v['weight'],
                        is_active=raw in ['1', 'true', 'on', True]
                    )
            
            return redirect('products:list')
    else:
        product_form = ProductForm()
        
        return render(request, 'products/create.html', {
            'product_form' : product_form,
            'sizes' : sizes,
            'colors' : colors,
        })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/detail.html', {'product' : product})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        variant_formset = ProductVariantFormSet(request.POST, instance=product)

        if product_form.is_valid() and variant_formset.is_valid():
            product_form.save()
            variant_formset.save()
            return redirect('products:list')
    else:
        product_form = ProductForm(instance=product)
        variant_formset = ProductVariantFormSet(instance=product)
    
    return render(request, 'products/create.html', {
        'product_form': product_form,
        'variant_formset': variant_formset
    })


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('products:list')
    
    return render(request, 'products/confirm_delete.html', {'product': product})