# backend/apps/finance/serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import FeeType, Fee, Invoice, InvoiceItem, Payment, PaymentGateway

class FeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeType
        fields = '__all__'
        read_only_fields = ('school',)

class FeeSerializer(serializers.ModelSerializer):
    fee_type_name = serializers.CharField(source='fee_type.name', read_only=True)
    
    class Meta:
        model = Fee
        fields = '__all__'
        read_only_fields = ('school',)

class InvoiceItemSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tax_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        read_only_fields = ('school',)

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    balance_due = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('school', 'invoice_number', 'total_amount', 'paid_amount')

class PaymentSerializer(serializers.ModelSerializer):
    invoice_number = serializers.CharField(source='invoice.invoice_number', read_only=True)
    student_name = serializers.CharField(source='invoice.student.get_full_name', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('school', 'reference', 'transaction_id')

class PaymentGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateway
        fields = '__all__'
        read_only_fields = ('school',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Masquer les clés sensibles
        if 'api_key' in representation:
            representation['api_key'] = '••••••••' + representation['api_key'][-4:] if representation['api_key'] else ''
        if 'secret_key' in representation:
            representation['secret_key'] = '••••••••' + representation['secret_key'][-4:] if representation['secret_key'] else ''
        if 'webhook_secret' in representation:
            representation['webhook_secret'] = '••••••••' + representation['webhook_secret'][-4:] if representation['webhook_secret'] else ''
        return representation