from django.db import models
from django.conf import settings
from students.models import Student
from django.utils import timezone

class Transaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    bank_name = models.CharField(max_length=50)
    deposit_slip = models.FileField(upload_to='')
    transaction_date = models.DateField()
    logged_by = models.CharField(max_length=50)

    # New approval fields
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name="verified_transactions"
    )
    verified_at = models.DateTimeField(null=True, blank=True)

    def verify(self, user):
        """Helper method to approve/verify a transaction"""
        self.is_verified = True
        self.verified_by = user
        self.verified_at = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        # Only update student balance if transaction is verified
        if self.is_verified:
            self.student.total_paid += self.amount_paid
            self.student.save()
        super().save(*args, **kwargs)

    def __str__(self):
        status = "✅ Verified" if self.is_verified else "⏳ Pending"
        return f"{self.student.full_name} - {self.amount_paid} on {self.transaction_date} [{status}]"
