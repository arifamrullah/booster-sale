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

def variant_empty_form(request):
    formset = ProductVariantFormSet(prefix='variants')
    empty_form = formset.empty_form

    html = render_to_string(
        'products/partials/variant_form.html',
        {'form' : empty_form}
    )

    return HttpResponse(html)

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products' : products})

def product_create(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        variant_formset = ProductVariantFormSet(request.POST)

        if product_form.is_valid() and variant_formset.is_valid():
            product = product_form.save()
            variant_formset.instance = product
            variant_formset.save()
            return redirect('products:list')
    else:
        product_form = ProductForm()
        variant_formset = ProductVariantFormSet()
        
    return render(request, 'products/create.html', {
        'product_form' : product_form,
        'variant_formset' : variant_formset
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