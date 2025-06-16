from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Branch, Order, Product, Production, Packing, ProductOrder

import json

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def inventory(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        max_rows = body.get('max_rows', None)
        try:
            fields = body.get('fields', [])
            qs = Packing.objects.select_related('product').values(*fields)
            if max_rows is not None:
                try:
                    max_rows = int(max_rows)
                    qs = qs[:max_rows]
                except (ValueError, TypeError):
                    pass  # Ignore invalid max_rows and return all
            data = qs
            return JsonResponse({'status': 'ok', 'data': list(data)}, status=200)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'An error occurred while processing your request.'}, status=400)
        
    elif request.method == 'GET':
        return JsonResponse({
            'status': 'error',
            'message': 'GET method is not supported for this endpoint. Please use POST with the required parameters.'
        }, status=200)

def packing(request):

    if request.method == 'POST':
        body = json.loads(request.body)
        max_rows = body.get('max_rows', None)
        try:
            fields = body.get('fields', [])
            qs = Packing.objects.select_related('product').values(*fields)
            if max_rows is not None:
                try:
                    max_rows = int(max_rows)
                    qs = qs[:max_rows]
                except (ValueError, TypeError):
                    pass  # Ignore invalid max_rows and return all
            data = qs
            return JsonResponse({'status': 'ok', 'data': list(data)}, status=200)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'An error occurred while processing your request.'}, status=400)
        
    elif request.method == 'GET':
        return JsonResponse({
            'status': 'error',
            'message': 'GET method is not supported for this endpoint. Please use POST with the required parameters.'
        }, status=200)