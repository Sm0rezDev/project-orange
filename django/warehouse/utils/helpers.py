from ..models import Product
from django.http import JsonResponse


def productId_lookup(product):
    if isinstance(product, str):
        try:
            product_obj = Product.objects.get(name__iexact=product)
            return product_obj.product_id
        except Product.DoesNotExist as e:
            raise ValueError(f"Product '{product}' does not exist.") from e
    else:
        return product