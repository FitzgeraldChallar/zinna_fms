from django.contrib import admin
from .models import Student

# Set the site title
admin.site.site_header = "Zinnah Child Development Academy Financial Monitoring System"
admin.site.site_title = "Zinnah Academy FMS"
admin.site.index_title = "Welcome to Zinnah Academy's Financial Monitoring System"

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'grade', 'total_fees', 'total_paid', 'balance')
    list_filter = ('grade',)  # Enables filtering by grade in sidebar
    search_fields = ('full_name', 'student_id')

    # Order the list alphabetically by full_name
    ordering = ('full_name',)
