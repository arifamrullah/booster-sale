from django.db import models

class Size(models.Model):
    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=50)

    class Meta:
        db_table = 'sizes'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} | {self.label}"