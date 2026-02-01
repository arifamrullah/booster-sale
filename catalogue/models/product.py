from django.db import models
from .category import Category

def product_main_image_path(instance, filename):
    return f'products/main/product_{instance.id}/{filename}'

class Product(models.Model):
    category_id = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to=product_main_image_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name