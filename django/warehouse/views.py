from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Branch, Order, Product, Production, Packing, ProductOrder

# Create your views here.

def inventory(request):
    return JsonResponse({'status': 'ok', 'message':''}, status=200)

def packing(request):
    
    # Placeholder response for the packing page
    return HttpResponse("Packing page is under construction. Please check back later.")