# Generated by Django 4.2 on 2024-06-12 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ata_api', '0002_rename_created_at_bill_issued_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='total_amount',
            new_name='amount',
        ),
    ]
