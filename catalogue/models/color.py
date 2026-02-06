from django.db import models

class Color(models.model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='colors/', null=True, blank=True)

    class Meta:
        db_table = 'colors'
        ordering = ['name']

    def __str__(self):
        return self.name