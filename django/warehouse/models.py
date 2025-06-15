from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100, default='Rosersberg')

    def __str__(self):
        return self.name

class Group(models.Model):
    group = models.CharField(max_length=10, default='#0')

    def __str__(self):
        return self.group

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Production(models.Model):
    production_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productions')
    batch = models.CharField(max_length=50, default='PROD0000000000', null=True)
    lot = models.CharField(max_length=50, default='0', null=True)

    def __str__(self):
        return f"{self.product.name} batch {self.batch}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed')
    ]
    order_id = models.AutoField(primary_key=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(default='2025-01-01', null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CREATED', null=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"

class Packing(models.Model):
    packing_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='packings')
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='packings')
    quantity = models.IntegerField(default=0, null=True)
    packing_date = models.DateField(default='2025-01-01', null=True)
    best_before = models.DateField(default='2025-01-01', null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product_id', 'production_id'], name='unique_product_production')
        ]

    def __str__(self):
        return f"Packing {self.product.name} from {self.production.batch}"

class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='product_orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_orders')
    quantity = models.IntegerField(default=0, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'product'], name='unique_order_product')
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product_id.name} in Order {self.order_id.order_id}"