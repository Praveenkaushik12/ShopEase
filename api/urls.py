from django.urls import include,path
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet,
    ProductViewSet,
    CartViewSet,
    OrderPlacedViewSet
)

router=DefaultRouter()
router.register(r'customers',CustomerViewSet)
router.register(r'products',ProductViewSet)
router.register(r'cart',CartViewSet)
router.register(r'orders',OrderPlacedViewSet)

urlpatterns = [
    path('',include(router.urls)),
]
