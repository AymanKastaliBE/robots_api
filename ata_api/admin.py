from django.contrib import admin
from . import models

class StaffAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "email"]

admin.site.register(models.Staff, StaffAdmin)


class BillAdmin(admin.ModelAdmin):
    list_display = ["id", "staff", "issued_at", "total_amount", "scanned_pdf"]

admin.site.register(models.Bill, BillAdmin)


class BalanceAdmin(admin.ModelAdmin):
    list_display = ["value", "updated_at"]

admin.site.register(models.Balance, BalanceAdmin)