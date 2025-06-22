from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.index),
    path('status/', views.status),
    path('production/new/', views.add_production),
    path('packing/', views.add_packing),
    path('order/new/', views.add_order),
]