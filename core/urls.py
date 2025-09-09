from django.contrib import admin
from django.urls import path, include  # Include is useful if you have app-level URLs
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),
    # You can also add other app routes like:
    # path('students/', include('students.urls')),
    # path('transactions/', include('transactions.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
