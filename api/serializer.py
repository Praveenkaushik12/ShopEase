from rest_framework import serializers
from app.models import (
    Customer,
    Product,
    Cart,
    OrderPlaced
)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields='__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
    
class CartSerializer(serializers.ModelSerializer):
    total_cost=serializers.ReadOnlyField()
    class Meta:
        model=Cart
        fields='__all__'
        
class OrderedPlacedSerializer(serializers.ModelSerializer):
    total_cost=serializers.ReadOnlyField()
    
    class Meta:
        model=OrderPlaced
        fields='__all__'
        
        