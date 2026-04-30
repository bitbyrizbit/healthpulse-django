from rest_framework import serializers
from .models import Doctor, Appointment


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_spec = serializers.CharField(source='doctor.specialization', read_only=True)
    patient_name = serializers.CharField(source='patient.username', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'doctor_spec', 'date', 'time_slot', 'reason', 'status', 'created_at'
        ]
        read_only_fields = ['patient', 'created_at']

    def create(self, validated_data):
        # auto-assign logged-in user as patient
        validated_data['patient'] = self.context['request'].user
        return super().create(validated_data)