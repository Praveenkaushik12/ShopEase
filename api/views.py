from django.shortcuts import render
from rest_framework import viewsets
from app.models import (
    Customer,
    Product,
    Cart,
    OrderPlaced
)
from .serializer import (
    CustomerSerializer,
    ProductSerializer,
    CartSerializer,
    OrderedPlacedSerializer
)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    
class CartViewSet(viewsets.ModelViewSet):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer
    
class OrderPlacedViewSet(viewsets.ModelViewSet):
    queryset=OrderPlaced.objects.all()
    serializer_class=OrderedPlacedSerializer
    
    
    
    


