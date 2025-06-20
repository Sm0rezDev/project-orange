from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Production, Packing

from datetime import date, timedelta
import json

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt # remove this in production, use proper CSRF protection
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
        
    elif request.method == 'GET':
        return JsonResponse({
            'status': 'error',
            'message': 'GET method is not supported for this endpoint. Please use POST with the required parameters.'
        }, status=200)
