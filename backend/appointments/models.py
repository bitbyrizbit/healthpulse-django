from django.db import models
from django.conf import settings

SPECIALIZATION_CHOICES = [
    ('general', 'General Physician'),
    ('cardio', 'Cardiologist'),
    ('ortho', 'Orthopedician'),
    ('neuro', 'Neurologist'),
    ('derma', 'Dermatologist'),
    ('endo', 'Endocrinologist'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
]


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    hospital = models.CharField(max_length=150)
    available_days = models.CharField(max_length=100, default='Mon-Sat')
    fee = models.DecimalField(max_digits=7, decimal_places=2, default=500.00)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"


class Appointment(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time_slot = models.TimeField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient.username} → Dr. {self.doctor.name} on {self.date}"