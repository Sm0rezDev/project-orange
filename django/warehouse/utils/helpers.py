from ..models import Product, Restaurant
from django.http import JsonResponse
from django.apps import apps

def get_model_class(app_label, model_name):
    try:
        return apps.get_model(app_label, model_name)
    except LookupError as e:
        raise ValueError(f"Model '{model_name}' in app '{app_label}' does not exist.") from e

def productId_lookup(product):
    if isinstance(product, str):
        try:
            product_obj = Product.objects.get(name__iexact=product)
            return product_obj.product_id
        except Product.DoesNotExist as e:
            raise ValueError(f"Product '{product}' does not exist.") from e
    else:
        return product
