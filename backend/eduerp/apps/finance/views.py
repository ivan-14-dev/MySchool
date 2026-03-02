from django.shortcuts import render

# Create your views here.
# backend/apps/finance/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, Sum

from .models import FeeType, Fee, Invoice, InvoiceItem, Payment, PaymentGateway
from .serializers import (
    FeeTypeSerializer, FeeSerializer, InvoiceSerializer,
    InvoiceItemSerializer, PaymentSerializer, PaymentGatewaySerializer
)
from apps.core.permissions import SchoolPermission, HasPermission

class FeeTypeViewSet(viewsets.ModelViewSet):
    queryset = FeeType.objects.all()
    serializer_class = FeeTypeSerializer
    permission_classes = [SchoolPermission, HasPermission(['finance.manage_fees'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']

class FeeViewSet(viewsets.ModelViewSet):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer
    permission_classes = [SchoolPermission, HasPermission(['finance.manage_fees'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['fee_type', 'academic_year', 'class_level', 'is_active', 'is_optional']

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [SchoolPermission, HasPermission(['finance.manage_invoices'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'status', 'academic_year', 'issue_date', 'due_date']
    
    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        invoice = self.get_object()
        invoice.status = 'paid'
        invoice.paid_amount = invoice.total_amount - invoice.discount
        invoice.save()
        return Response({'status': 'invoice marked as paid'})
    
    @action(detail=True, methods=['post'])
    def send_reminder(self, request, pk=None):
        invoice = self.get_object()
        # Logique d'envoi de rappel
        return Response({'status': 'reminder sent'})
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        total_invoices = Invoice.objects.count()
        total_paid = Invoice.objects.filter(status='paid').aggregate(total=Sum('total_amount'))['total'] or 0
        total_pending = Invoice.objects.filter(status='sent').aggregate(total=Sum('total_amount'))['total'] or 0
        total_overdue = Invoice.objects.filter(status='overdue').aggregate(total=Sum('total_amount'))['total'] or 0
        
        return Response({
            'total_invoices': total_invoices,
            'total_paid': total_paid,
            'total_pending': total_pending,
            'total_overdue': total_overdue
        })

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [SchoolPermission, HasPermission(['finance.manage_payments'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['invoice', 'method', 'status', 'payment_date']

class PaymentGatewayViewSet(viewsets.ModelViewSet):
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer
    permission_classes = [SchoolPermission, HasPermission(['finance.manage_gateways'])]
    
    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        gateway = self.get_object()
        # Logique de test de connexion
        return Response({'status': 'connection successful'})