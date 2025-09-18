from django.contrib import admin
from django.utils import timezone
from .models import Transaction, Student

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'amount_paid', 'currency', 'payment_type', 
        'bank_name', 'transaction_date', 'logged_by', 
        'is_verified', 'verified_by', 'verified_at'
    ]
    search_fields = ['student__full_name', 'payment_type']
    list_filter = ['bank_name', 'transaction_date', 'is_verified']

    # Custom admin action to verify transactions
    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        for transaction in queryset.filter(is_verified=False):
            transaction.is_verified = True
            transaction.verified_by = request.user
            transaction.verified_at = timezone.now()
            transaction.student.total_paid += transaction.amount_paid
            transaction.student.save()
            transaction.save()
        self.message_user(request, "Selected transactions have been verified.")

    mark_as_verified.short_description = "Verify selected transactions"

    # Order the student dropdown alphabetically by full_name
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = Student.objects.all().order_by('full_name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_change_permission(self, request, obj=None):
        # Only allow users in 'Admin' group to change/verify transactions
        if request.user.groups.filter(name="Admin").exists():
           return True
        return False
    
    # ✅ Make is_verified read-only for registrars
    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser and not request.user.groups.filter(name="Admin").exists():
            readonly.append("is_verified")
        return readonly

