from django.db import models

class Student(models.Model):
    GRADE_CHOICES = [
        ('3', '3rd Grade'),
        ('4', '4th Grade'),
        ('5', '5th Grade'),
        ('6', '6th Grade'),
        ('7', '7th Grade'),
    ]
    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.balance = self.total_fees - self.total_paid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.grade}"
