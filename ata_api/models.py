from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
import uuid
from django.urls import reverse


class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phonenumber = PhoneNumberField(blank=True)
    job_title = models.CharField(max_length=32, blank=True, null=True)
    contract_end_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return str(self.name)


class Bill(models.Model):
    EXPENSE = 'expense'
    RECHARGE = 'recharge'
    
    TYPE_CHOICES = [
        (EXPENSE, 'Expense'),
        (RECHARGE, 'Recharge'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=EXPENSE, null=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    issued_at = models.DateField(blank=True, null=True)
    supplier_name = models.CharField(max_length=256, blank=True, null=True)
    invoice_number = models.CharField(max_length=128, blank=True, null=True)
    transaction_number = models.CharField(max_length=128, blank=True, null=True)
    vat = models.DecimalField(max_digits=7, decimal_places=2, default=0, blank=True, null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0, blank=True, null=True)
    remark = models.DecimalField(max_digits=7, decimal_places=2, default=0, blank=True, null=True)
    scanned_pdf = models.FileField(upload_to='docs/', blank=True, null=True)
    
    def __str__(self):
        return str(self.id)
    
    def get_absolute_url(self):
        return reverse('ata_api:bill_detail_view', args=[str(self.id)])
    
    
class Balance(models.Model):
    value = models.DecimalField(max_digits=7, decimal_places=2, default=0, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return str(self.value)
    
    
class ReceivedCash(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=7, decimal_places=2, default=0, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return str(self.value)
    