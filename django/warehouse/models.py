from django.db import models

class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group = models.CharField(max_length=10, default='#0')

    def __str__(self):
        return self.group

class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, null=True, default=None)


    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Production(models.Model):
    production_id = models.AutoField(primary_key=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='productions')
    batch = models.CharField(max_length=50, null=True)
    lot = models.CharField(max_length=50, null=True)
    volume = models.FloatField(null=True)

    def __str__(self):
        return f"Batch {self.batch} Lot {self.lot}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed')
    ]
    order_id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CREATED')

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"

class Packing(models.Model):
    packing_id = models.AutoField(primary_key=True)
    production = models.OneToOneField(Production, on_delete=models.CASCADE, related_name='packings')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='packings')
    packing_date = models.DateField(null=True)
    best_before = models.DateField(null=True)
    quantity = models.IntegerField(default=0, null=True)

    class Meta:
        unique_together = (('production', 'product'),)

    def __str__(self):
        return f"Packing {self.packing_id} from Production {self.production_id}"

class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='product_orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_orders')
    quantity = models.IntegerField(default=0, null=True)

    class Meta:
        unique_together = (('order', 'product'),)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"