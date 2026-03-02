# backend/apps/finance/admin.py
from django.contrib import admin
from .models import FeeType, Fee, Invoice, InvoiceItem, Payment, PaymentGateway

@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    list_filter = ('is_active', 'school')
    search_fields = ('name', 'code')

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'fee_type', 'amount', 'due_date', 'is_active')
    list_filter = ('fee_type', 'academic_year', 'class_level', 'is_active')
    search_fields = ('name', 'fee_type__name')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'student', 'total_amount', 'paid_amount', 'status', 'due_date')
    list_filter = ('status', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'student__first_name', 'student__last_name')
    readonly_fields = ('invoice_number', 'total_amount')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reference', 'invoice', 'amount', 'method', 'status', 'payment_date')
    list_filter = ('method', 'status', 'payment_date')
    search_fields = ('reference', 'invoice__invoice_number')

@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'is_active', 'test_mode')
    list_filter = ('type', 'is_active', 'test_mode')