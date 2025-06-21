from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Product, Production, Packing

from datetime import date, timedelta
import json

from django.middleware.csrf import get_token

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

# Create your views here.

# This view handles the status of products and productions.
def status(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        table = body.get('table', 'products')
        fields = body.get('fields', [])
        max_rows = body.get('max_rows', None)
        
        data = []

        try:
            def validate_fields(row, forbidden_prefix):
                for key in list(row.keys()):
                    if key.startswith(forbidden_prefix):
                        return False
                return True

            if table == 'products':
                qs = Packing.objects.select_related('product').values(*fields)
                forbidden_prefix = 'production__'
            elif table == 'productions':
                qs = Production.objects.select_related('packing').values(*fields)
                forbidden_prefix = 'product__'
            else:
                qs = None

            if qs is not None:
                for row in qs:
                    if not validate_fields(row, forbidden_prefix):
                        return JsonResponse({
                            'status': 'error',
                            'message': f'Invalid field specified. Fields starting with "{forbidden_prefix}" are not allowed.'
                        }, status=400)
                    new_row = dict(row)
                    if "product__name" in new_row:
                        new_row["product_name"] = new_row.pop("product__name")
                    data.append(new_row)

            else:
                return JsonResponse({
                    'status': 'Table not found',
                    'message': 'Invalid table specified. Please use "products" or "productions".'
                }, status=400)
            
            if max_rows is not None:
                try:
                    max_rows = int(max_rows)
                    qs = qs[:max_rows]
                except (ValueError, TypeError):
                    pass  # Ignore invalid max_rows and return all

            #data = qs

            return JsonResponse({'status': 'success', 'data': list(data)}, status=200)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'An error occurred while processing your request.'}, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'GET method is not supported for this endpoint. Please use POST with the required parameters.'
    }, status=200)

# This view handles the addition of a new production record.
def add_production(request):
    if request.method == 'POST':
        # CSRF token can be accessed if needed, but do not modify request.headers
        body = json.loads(request.body)
        product_id = body.get('product_id')

        if isinstance(product_id, str):
            # If product_id is a string, assume it's the product name
            # and fetch the product id
            product = Product.objects.get(name__iexact=product_id)
            product_id = product.product_id
        else:
            pass

        batch = body.get('batch')
        lot = body.get('lot')
        volume = body.get('volume', 0.0)

        if not all([product_id, batch, lot, volume]):
            return JsonResponse({'status': 'error', 'message': 'Missing required parameters: product_id, batch, lot, and volume are required.'}, status=400)
        if not isinstance(volume, (int, float)):
            return JsonResponse({'status': 'error', 'message': 'Volume must be a number.'}, status=400)
        if volume < 0:
            return JsonResponse({'status': 'error', 'message': 'Volume cannot be negative.'}, status=400)

        try:
            production = Production.objects.create(
                product_id=product_id,
                batch=batch,
                lot=lot,
                volume=volume
            )
            return JsonResponse({'status': 'success', 'production_id': production.production_id}, status=201)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
    return JsonResponse({'status': 'error', 'message': 'GET method is not supported for this endpoint. Please use POST with the required parameters.'}, status=405)

# This view handles the addition of a new packing record.
def add_packing(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        production_id = body.get('production_id')
        product_id = body.get('product_id')
        packing_date = body.get('packing_date', date.today())
        best_before = packing_date + timedelta(days=365)  # Default to 1 year later
        print(f"Packing date: {packing_date}, Best before: {best_before}")
        quantity = body.get('quantity', 0.0)

        if isinstance(product_id, str):
            # If product_id is a string, assume it's the product name
            # and fetch the product id
            product = Product.objects.get(name__iexact=product_id)
            product_id = product.product_id
        else:
            pass

        if isinstance(production_id, str):
            # If production_id is a string, assume it's the production batch
            # and fetch the production id
            production = Production.objects.get(batch__iexact=product_id)
            production_id = production.production_id
        else:
            pass
        
        if not all([production_id, product_id, quantity]):
            return JsonResponse({'status': 'error', 'message': 'Missing required parameters: production_id, product_id, and quantity are required.'}, status=400)
        if not isinstance(quantity, (int, float)):
            return JsonResponse({'status': 'error', 'message': 'Quantity must be a number.'}, status=400)
        if quantity < 0:
            return JsonResponse({'status': 'error', 'message': 'Quantity cannot be negative.'}, status=400)

        try:
            packing = Packing.objects.create(
                production_id=production_id,
                product_id=product_id,
                packing_date=packing_date,
                best_before=best_before,
                quantity=quantity
            )
            return JsonResponse({'status': 'success', 'packing_id': packing.packing_id}, status=201)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'GET method is not supported for this endpoint. Please use POST with the required parameters.'}, status=405)