from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('appointments.urls')),
    path('health/', include('health.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/health/', include('health.urls')),
]