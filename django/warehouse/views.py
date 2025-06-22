from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Production, Packing, Restaurant, Order, ProductOrder

from datetime import date, timedelta, datetime
import json

from .utils.helpers import productId_lookup

def index(request):
    if request.method == 'GET':
        return JsonResponse({'status': 'success', 'message': 'CSRF token is set!'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed.'}, status=405)

def status(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'GET method forbidden, use POST.'}, status=405)
    try:
        body = json.loads(request.body)
        table = body.get('table', 'products')
        fields = body.get('fields', [])
        max_rows = body.get('max_rows')
        data = []

        def validate_fields(row, forbidden_prefix):
            return not any(key.startswith(forbidden_prefix) for key in row.keys())

        qs, forbidden_prefix = None, ''
        if table == 'products':
            qs = Packing.objects.select_related('product').values(*fields)
            forbidden_prefix = 'production__'
        elif table == 'productions':
            qs = Production.objects.select_related('packing').values(*fields)
            forbidden_prefix = 'product__'
        elif table == 'orders':
            qs = ProductOrder.objects.select_related('order', 'product').values(*fields)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid table.'}, status=400)

        if max_rows:
            try:
                max_rows = int(max_rows)
                qs = qs[:max_rows]
            except (ValueError, TypeError):
                pass

        for row in qs:
            if forbidden_prefix and not validate_fields(row, forbidden_prefix):
                return JsonResponse({'status': 'error', 'message': f'Fields starting with "{forbidden_prefix}" not allowed.'}, status=400)
            
            new_row = dict(row)
            remapp(data, new_row)

        return JsonResponse({'status': 'success', 'data': data}, status=200)
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'Processing error.'}, status=400)

def remapp(data, new_row):
    if "product__name" in new_row:
        new_row["product_name"] = new_row.pop("product__name")

    if "order__created_at" in new_row:
        new_row["created_at"] = new_row.pop("order__created_at")

    if "order__restaurant__city" in new_row:
        new_row["city"] = new_row.pop("order__restaurant__city")

    if "order__restaurant__district" in new_row:
        new_row["district"] = new_row.pop("order__restaurant__district")

    if "order__status" in new_row:
        new_row["status"] = new_row.pop("order__status")
                
    data.append(new_row)

def add_production(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)
    try:
        body = json.loads(request.body)
        product_id = body.get('product_id')
        if isinstance(product_id, str):
            product = Product.objects.get(name__iexact=product_id)
            product_id = product.product_id

        batch = body.get('batch')
        lot = body.get('lot')
        volume = body.get('volume', 0.0)

        if not all([product_id, batch, lot, volume]):
            return JsonResponse({'status': 'error', 'message': 'Missing required parameters.'}, status=400)
        if not isinstance(volume, (int, float)) or volume < 0:
            return JsonResponse({'status': 'error', 'message': 'Volume must be a non-negative number.'}, status=400)

        production = Production.objects.create(
            product_id=product_id,
            batch=batch,
            lot=lot,
            volume=volume
        )
        return JsonResponse({'status': 'success', 'production_id': production.production_id}, status=201)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def add_packing(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)
    try:
        body = json.loads(request.body)
        production_id = body.get('production_id')
        product_id = body.get('product_id')
        packing_date = body.get('packing_date', str(date.today()))
        packing_date = datetime.strptime(packing_date, '%Y-%m-%d').date() if isinstance(packing_date, str) else packing_date
        best_before = packing_date + timedelta(days=365)
        quantity = body.get('quantity', 0.0)

        if isinstance(product_id, str):
            product = Product.objects.get(name__iexact=product_id)
            product_id = product.product_id

        if isinstance(production_id, str):
            production = Production.objects.get(batch__iexact=production_id)
            production_id = production.production_id

        if not all([production_id, product_id, quantity]):
            return JsonResponse({'status': 'error', 'message': 'Missing required parameters.'}, status=400)
        if not isinstance(quantity, (int, float)) or quantity < 0:
            return JsonResponse({'status': 'error', 'message': 'Quantity must be a non-negative number.'}, status=400)

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

def add_order(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)
    try:
        body = json.loads(request.body)
        restaurant_id = body.get('restaurant_id')
        city = body.get('city')
        district = body.get('district')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        products = body.get('products', [])

        provided = [bool(restaurant_id), bool(city), bool(district)]
        if sum(provided) != 1:
            return JsonResponse({'status': 'error', 'message': 'Provide exactly one of restaurant_id, city, or district.'}, status=400)

        if city:
            try:
                restaurant = Restaurant.objects.get(city__iexact=city)
                restaurant_id = restaurant.restaurant_id
            except Restaurant.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': f'No restaurant found in city: {city}'}, status=404)
        if district:
            try:
                restaurant = Restaurant.objects.get(district__iexact=district)
                restaurant_id = restaurant.restaurant_id
            except Restaurant.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': f'No restaurant found in district: {district}'}, status=404)

        order = Order.objects.create(
            restaurant_id=restaurant_id,
            created_at=timestamp,
            status='CREATED'
        )

        product_orders = []
        if isinstance(products, list):
            for product in products:
                if isinstance(product, dict):
                    product_id = productId_lookup(product['product'])
                    product_quantity = product['quantity']
                    product_orders.append(ProductOrder(
                        order=order,
                        product_id=product_id,
                        quantity=product_quantity
                    ))
        ProductOrder.objects.bulk_create(product_orders)
        return JsonResponse({'status': 'success', 'message': 'Order created'}, status=201)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
