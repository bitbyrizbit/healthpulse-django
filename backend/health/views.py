import requests as http_requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import HealthRecord
from .serializers import HealthRecordSerializer

FASTAPI_URL = "http://127.0.0.1:8001"


@login_required
def checker_view(request):
    if request.method == 'POST':
        data = {
            'age': int(request.POST.get('age')),
            'weight_kg': float(request.POST.get('weight_kg')),
            'height_cm': float(request.POST.get('height_cm')),
            'systolic_bp': int(request.POST.get('systolic_bp')),
            'diastolic_bp': int(request.POST.get('diastolic_bp')),
            'blood_sugar': float(request.POST.get('blood_sugar')),
            'cholesterol': float(request.POST.get('cholesterol')),
            'smoker': request.POST.get('smoker') == 'on',
            'diabetic': request.POST.get('diabetic') == 'on',
        }

        # Call FastAPI ML service (Exp 13)
        try:
            ml_resp = http_requests.post(f"{FASTAPI_URL}/predict", json=data, timeout=5)
            ml_data = ml_resp.json()
            risk_score = ml_data.get('risk_score', 0.5)
            risk_label = ml_data.get('risk_label', 'Moderate')
        except Exception:
            risk_score = None
            risk_label = 'Unavailable'

        record = HealthRecord.objects.create(
            user=request.user,
            risk_score=risk_score,
            risk_label=risk_label,
            **data
        )
        return redirect(f'/health/result/{record.id}/')

    return render(request, 'health/checker.html')


@login_required
def result_view(request, pk):
    record = HealthRecord.objects.get(pk=pk, user=request.user)
    return render(request, 'health/result.html', {'record': record})


# DRF
class HealthRecordViewSet(viewsets.ModelViewSet):
    serializer_class = HealthRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HealthRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)