from django.db import models
from .product import Product

def product_main_image_path(instance, filename):
    return f"products/main/product_{instance.id}/{filename}"

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to=product_main_image_path)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_images'

    def __str__(self):
        return f"Image of {self.product.name}"