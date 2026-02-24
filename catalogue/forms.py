from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError
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

        widgets = {
            'has_variant': forms.CheckboxInput(attrs={
                'v-model': 'hasVariant'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = Category.objects.filter(parent__isnull=False)

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['color', 'size', 'sku', 'price', 'stock', 'weight', 'is_active']

    def clean_sku(self):
        sku = self.cleaned_data['sku']
        if not sku:
            raise forms.ValidationError('SKU wajib diisi')
        return sku

class BaseVariantFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        if not self.instance.has_variant:
            return

        active_forms = [
            form for form in self.forms
            if form.has_changed() and not form.cleaned_data.get('DELETE', False)
        ]

        if not active_forms:
            raise ValidationError('Varian can not be empty')
        
        sku_set = set()
        for form in active_forms:
            sku = form.cleaned_data.get('sku')
            if sku in sku_set:
                raise ValidationError('SKU can not duplicate')
            sku_set.add(sku)

ProductVariantFormSet = inlineformset_factory(
    Product,
    ProductVariant,
    form=ProductVariantForm,
    formset=BaseVariantFormSet,
    extra=1,
    can_delete=False
)