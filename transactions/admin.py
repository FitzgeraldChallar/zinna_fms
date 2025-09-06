from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount_paid', 'currency', 'payment_type', 'bank_name', 'transaction_date', 'logged_by']
    search_fields = ['student__full_name', 'payment_type']
    list_filter = ['bank_name', 'transaction_date']
