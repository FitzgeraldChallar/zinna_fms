from django.contrib import admin
from .models import Transaction, Student

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount_paid', 'currency', 'payment_type', 'bank_name', 'transaction_date', 'logged_by']
    search_fields = ['student__full_name', 'payment_type']
    list_filter = ['bank_name', 'transaction_date']

    # Order the student dropdown alphabetically by full_name
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = Student.objects.all().order_by('full_name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
