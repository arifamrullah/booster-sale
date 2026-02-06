from django.db import models
from django.db.models import Q
from .product import Product
from .size import Size
from .color import Color

def product_variant_image_path(instance, filename):
    return f"products/variant/product_{instance.id}/{filename}"

class ProductVariant(models.model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.PROTECT,
        related_name='variants'
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.PROTECT,
        related_name='variants'
    )
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to=product_variant_image_path, null=True, blank=True)
    size_chest = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    size_body = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    size_sleeve = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    size_shoulder = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_add_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_variants'
        constraints = [
            models.UniqueConstraint(
                fields = ['product', 'size', 'color'],
                condition = Q(is_active=True),
                name = 'unique_active_product_variant'
            )
        ]

    def __str__(self):
        return f"{self.product} + {self.color} + {self.size}"