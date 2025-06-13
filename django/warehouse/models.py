from django.db import models

# Create your models here.

class Branch(models.Model):
    BranchID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100, default='Rosersberg')

class Orders(models.Model):
    OrderID = models.AutoField(primary_key=True)
    Created = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=50, choices=[
        ('CREATED', 'Created'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed')
    ])
    Branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

class Products(models.Model):
    ProductID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Group = models.CharField(max_length=3)

class Production(models.Model):
    ProductionID = models.AutoField(primary_key=True)
    Product = models.ForeignKey(Products, on_delete=models.CASCADE)
    Batch = models.CharField(max_length=50, default='0000')
    Date = models.DateField(auto_now_add=True)

class Packing(models.Model):
    Product = models.ForeignKey(Products, on_delete=models.CASCADE)
    Production = models.ForeignKey(Production, on_delete=models.CASCADE)
    Lot = models.CharField(max_length=50, default='0000')
    Quantity = models.IntegerField(default=0)
    Date = models.DateField(auto_now_add=True)
    BestBefore = models.DateField(auto_now_add=True)

class OrderProduct(models.Model):
    Order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    Product = models.ForeignKey(Products, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=0)