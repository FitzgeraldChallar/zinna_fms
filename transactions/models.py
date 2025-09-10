from django.db import models
from students.models import Student

class Transaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    bank_name = models.CharField(max_length=50)
    deposit_slip = models.FileField(upload_to='')
    transaction_date = models.DateField()
    logged_by = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        # Update student record upon transaction
        self.student.total_paid += self.amount_paid
        self.student.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.full_name} - {self.amount_paid} on {self.transaction_date}"
