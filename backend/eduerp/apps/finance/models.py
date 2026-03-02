# backend/apps/finance/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import SchoolAwareModel, BaseModel
from apps.users.models import User

class FeeType(SchoolAwareModel):
    """Type de frais scolaire"""
    name = models.CharField(_("fee type name"), max_length=255)
    code = models.CharField(_("fee type code"), max_length=50, unique=True)
    description = models.TextField(_("description"), blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    
    class Meta:
        verbose_name = _("fee type")
        verbose_name_plural = _("fee types")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Fee(SchoolAwareModel):
    """Frais scolaire"""
    FEE_FREQUENCY = (
        ('one_time', _('One-time')),
        ('monthly', _('Monthly')),
        ('quarterly', _('Quarterly')),
        ('yearly', _('Yearly')),
    )
    
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE, related_name='fees')
    name = models.CharField(_("fee name"), max_length=255)
    amount = models.DecimalField(_("amount"), max_digits=10, decimal_places=2)
    due_date = models.DateField(_("due date"))
    academic_year = models.CharField(_("academic year"), max_length=9)
    class_level = models.CharField(_("class level"), max_length=50, blank=True)
    frequency = models.CharField(_("frequency"), max_length=20, choices=FEE_FREQUENCY, default='one_time')
    is_optional = models.BooleanField(_("optional"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    
    class Meta:
        verbose_name = _("fee")
        verbose_name_plural = _("fees")
        ordering = ['due_date', 'class_level']

    def __str__(self):
        return f"{self.name} - {self.amount}€"


class Invoice(SchoolAwareModel):
    """Facture"""
    INVOICE_STATUS = (
        ('draft', _('Draft')),
        ('sent', _('Sent')),
        ('paid', _('Paid')),
        ('overdue', _('Overdue')),
        ('cancelled', _('Cancelled')),
        ('partial', _('Partially Paid')),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, 
                               limit_choices_to={'user_type': 'student'},
                               related_name='invoices')
    invoice_number = models.CharField(_("invoice number"), max_length=50, unique=True)
    issue_date = models.DateField(_("issue date"))
    due_date = models.DateField(_("due date"))
    status = models.CharField(_("status"), max_length=20, choices=INVOICE_STATUS, default='draft')
    total_amount = models.DecimalField(_("total amount"), max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(_("paid amount"), max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(_("discount"), max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(_("tax amount"), max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(_("notes"), blank=True)
    terms = models.TextField(_("terms"), blank=True)
    
    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")
        ordering = ['-issue_date']

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.student.get_full_name()}"

    @property
    def balance_due(self):
        return self.total_amount - self.paid_amount - self.discount

    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.due_date < timezone.now().date() and self.status not in ['paid', 'cancelled']


class InvoiceItem(SchoolAwareModel):
    """Ligne de facture"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name='invoice_items')
    description = models.CharField(_("description"), max_length=255)
    quantity = models.DecimalField(_("quantity"), max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(_("unit price"), max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(_("tax rate"), max_digits=5, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = _("invoice item")
        verbose_name_plural = _("invoice items")

    def __str__(self):
        return f"{self.description} - {self.quantity} x {self.unit_price}"

    @property
    def total_amount(self):
        return self.quantity * self.unit_price

    @property
    def tax_amount(self):
        return self.total_amount * (self.tax_rate / 100)


class Payment(SchoolAwareModel):
    """Paiement"""
    PAYMENT_METHODS = (
        ('cash', _('Cash')),
        ('check', _('Check')),
        ('transfer', _('Bank Transfer')),
        ('card', _('Credit Card')),
        ('online', _('Online Payment')),
        ('mobile_money', _('Mobile Money')),
    )
    
    PAYMENT_STATUS = (
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('refunded', _('Refunded')),
        ('cancelled', _('Cancelled')),
    )
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(_("amount"), max_digits=10, decimal_places=2)
    payment_date = models.DateField(_("payment date"))
    method = models.CharField(_("payment method"), max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(_("status"), max_length=20, choices=PAYMENT_STATUS, default='pending')
    reference = models.CharField(_("payment reference"), max_length=255, blank=True)
    transaction_id = models.CharField(_("transaction ID"), max_length=255, blank=True)
    notes = models.TextField(_("notes"), blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                   related_name='processed_payments')
    
    class Meta:
        verbose_name = _("payment")
        verbose_name_plural = _("payments")
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment #{self.reference} - {self.amount}€"


class PaymentGateway(SchoolAwareModel):
    """Configuration des passerelles de paiement"""
    GATEWAY_TYPES = (
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
    )
    
    name = models.CharField(_("gateway name"), max_length=100)
    type = models.CharField(_("gateway type"), max_length=20, choices=GATEWAY_TYPES)
    is_active = models.BooleanField(_("active"), default=False)
    test_mode = models.BooleanField(_("test mode"), default=True)
    api_key = models.CharField(_("API key"), max_length=255, blank=True)
    secret_key = models.CharField(_("secret key"), max_length=255, blank=True)
    webhook_secret = models.CharField(_("webhook secret"), max_length=255, blank=True)
    additional_config = models.JSONField(_("additional configuration"), default=dict)
    
    class Meta:
        verbose_name = _("payment gateway")
        verbose_name_plural = _("payment gateways")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"