from django.db import models
from django.conf import settings


class HealthRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='health_records'
    )
    age = models.IntegerField()
    weight_kg = models.FloatField()
    height_cm = models.FloatField()
    systolic_bp = models.IntegerField(help_text='e.g. 120')
    diastolic_bp = models.IntegerField(help_text='e.g. 80')
    blood_sugar = models.FloatField(help_text='mg/dL fasting')
    cholesterol = models.FloatField(help_text='mg/dL total')
    smoker = models.BooleanField(default=False)
    diabetic = models.BooleanField(default=False)
    # ML prediction result stored back
    risk_score = models.FloatField(null=True, blank=True)
    risk_label = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def bmi(self):
        h = self.height_cm / 100
        return round(self.weight_kg / (h * h), 1)

    def __str__(self):
        return f"{self.user.username} — {self.created_at.date()}"