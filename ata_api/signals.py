from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Bill, Balance

@receiver(post_save, sender=Bill)
def update_balance_on_save(sender, instance, created, **kwargs):
    if instance.type == 'expense':
        subtract_from_balance(instance.amount + instance.vat)
    elif instance.type == 'recharge':
        add_to_balance(instance.amount)

@receiver(post_delete, sender=Bill)
def update_balance_on_delete(sender, instance, **kwargs):
    if instance.scanned_pdf:
        instance.scanned_pdf.delete(save=False)
    if instance.type == 'expense':
        add_to_balance(instance.amount + instance.vat)
    elif instance.type == 'recharge':
        subtract_from_balance(instance.amount)
    


@receiver(pre_save, sender=Bill)
def update_balance_on_update(sender, instance, **kwargs):
    try:
        old_instance = Bill.objects.get(pk=instance.pk)
    except Bill.DoesNotExist:
        return

    old_instance_type = old_instance.type
    old_total = old_instance.amount + old_instance.vat
    # new_total = instance.amount + instance.vat
    # balance_change = new_total - old_total
    
    if old_instance_type == 'expense':
        add_to_balance(old_total)
    elif old_instance_type == "recharge":
        subtract_from_balance(old_total)


def subtract_from_balance(amount):
    balance = Balance.objects.first()
    if balance:
        balance.value -= amount
        balance.save()


def add_to_balance(amount):
    balance = Balance.objects.first()
    if balance:
        balance.value += amount
        balance.save()
        
