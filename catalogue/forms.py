from django import forms
from django.forms import inlineformset_factory
from .models.category import Category
from .models.product import Product
from .models.product_image import ProductImage
from .models.color import Color
from .models.size import Size
from .models.product_variant import ProductVariant

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'category', 'description', 'has_variant', 'price', 'stock', 'weight', 'is_active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = Category.objects.filter(parent__isnull=False)

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['sku', 'price', 'stock']

    def clean_sku(self):
        sku = self.cleaned_data['sku']
        if not sku:
            raise forms.ValidationError('SKU wajib diisi')
        return sku

ProductVariantFormSet = inlineformset_factory(
    Product,
    ProductVariant,
    form = ProductVariantForm,
    extra=1,
    can_delete=False
)