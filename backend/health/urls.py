from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'records', views.HealthRecordViewSet, basename='healthrecord')

urlpatterns = [
    path('checker/', views.checker_view, name='checker'),
    path('result/<int:pk>/', views.result_view, name='result'),
    path('api/', include(router.urls)),
]