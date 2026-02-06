from django.db import models
from .category import Category

def product_main_image_path(instance, filename):
    return f"products/main/product_{instance.id}/{filename}"

class Product(models.Model):
    image = models.ImageField(upload_to=product_main_image_path)
    name = models.CharField(max_length=300)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    sku = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-updated_at']

    def __str__(self):
        return self.name