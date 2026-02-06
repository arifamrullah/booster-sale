from django.db import models
from .category import Category

class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=300)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )
    description = models.TextField()
    has_variant = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0, null=True, blank=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-updated_at']

    def __str__(self):
        return self.name
    
    def clean(self):
        from django.core.exceptions import ValidationError

        if not self.has_variant:
            if self.price is None:
                raise ValidationError({'price': "Price Required"})
            if self.stock is None:
                raise ValidationError({'stock': "Stock Required"})
            if self.weight is None:
                raise ValidationError({'weight': "Weight Required"})