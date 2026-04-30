from rest_framework import serializers
from .models import HealthRecord


class HealthRecordSerializer(serializers.ModelSerializer):
    bmi = serializers.FloatField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = HealthRecord
        fields = [
            'id', 'username', 'age', 'weight_kg', 'height_cm', 'bmi',
            'systolic_bp', 'diastolic_bp', 'blood_sugar', 'cholesterol',
            'smoker', 'diabetic', 'risk_score', 'risk_label', 'created_at'
        ]
        read_only_fields = ['user', 'risk_score', 'risk_label', 'created_at']