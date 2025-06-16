from django.test import TestCase
from warehouse.models import Branch, Group, Product, Production, Order, Packing

# Create your tests here.

class WarehouseTestCase(TestCase):
    def setUp(self):
        self.branch = Branch.objects.create(name='Test Branch')
        self.group = Group.objects.create(group='#1')
        self.product = Product.objects.create(name='Test Product', group=self.group)
        self.production = Production.objects.create(product=self.product, batch='TESTBATCH', lot='12345')
        self.order = Order.objects.create(branch=self.branch, status='CREATED')
        self.packing = Packing.objects.create(product=self.product, production=self.production, quantity=10)

    def test_branch_creation(self):
        self.assertEqual(self.branch.name, 'Test Branch')

    def test_group_creation(self):
        self.assertEqual(self.group.group, '#1')

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.group, self.group)

    def test_production_creation(self):
        self.assertEqual(self.production.batch, 'TESTBATCH')
        self.assertEqual(self.production.lot, '12345')

    def test_order_creation(self):
        self.assertEqual(self.order.status, 'CREATED')
        self.assertEqual(self.order.branch, self.branch)

    def test_packing_creation(self):
        self.assertEqual(self.packing.quantity, 10)
        self.assertEqual(self.packing.product, self.product)