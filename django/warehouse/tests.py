from django.test import TestCase
from warehouse.models import Restaurant, Group, Product, Production, Order, Packing

# Create your tests here.

class WarehouseTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            city='Imaginary City',
            district='iamginary district'
        )
        self.group = Group.objects.create(group='#1')
        self.product = Product.objects.create(
            name='Imaginary product',
            group=self.group
        )
        self.production = Production.objects.create(
            product=self.product,
            batch='TESTBATCH001',
            lot='abc123',
            volume=100.0
        )
        self.order = Order.objects.create(
            restaurant=self.restaurant,
            created_at='2023-01-01T12:00:00Z',
            status='CREATED'
        )
        self.packing = Packing.objects.create(
            product=self.product,
            production=self.production,
            quantity=60
        )

    def test_retaurant_creation(self):
        self.assertEqual(self.restaurant.city, 'Imaginary City')

    def test_group_creation(self):
        self.assertEqual(self.group.group, '#1')

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Imaginary product')
        self.assertEqual(self.product.group, self.group)

    def test_production_creation(self):
        self.assertEqual(self.production.batch, 'TESTBATCH001')
        self.assertEqual(self.production.lot, 'abc123')

    def test_order_creation(self):
        self.assertEqual(self.order.status, 'CREATED')
        self.assertEqual(self.order.restaurant.city, 'Imaginary City')

    def test_packing_creation(self):
        self.assertEqual(self.packing.quantity, 60)
        self.assertEqual(self.packing.product, self.product)