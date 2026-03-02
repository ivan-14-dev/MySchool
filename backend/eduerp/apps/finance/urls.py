# backend/apps/finance/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FeeTypeViewSet, FeeViewSet, InvoiceViewSet,
    PaymentViewSet, PaymentGatewayViewSet
)

router = DefaultRouter()
router.register(r'fee-types', FeeTypeViewSet)
router.register(r'fees', FeeViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'payment-gateways', PaymentGatewayViewSet)

urlpatterns = [
    path('', include(router.urls)),
]