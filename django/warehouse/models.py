from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

class ProductBatch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ProductionDate = models.DateField()
    ExpiryDate = models.DateField()
    lot_number = models.IntegerField
    batch_number = models.CharField(max_length=50)
    quantity = models.IntegerField()