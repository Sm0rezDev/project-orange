from django.db import models

# Create your models here.

class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='Rosersberg')

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('CREATED', 'Created'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed')
    ])

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=3)

class Productions(models.Model):
    production_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    batch = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

class Packing(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    production = models.ForeignKey(Productions, on_delete=models.CASCADE)
    lot = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    best_before = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = (('product', 'production', 'lot'),)

class ProductOrder(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = (('order', 'product'),)