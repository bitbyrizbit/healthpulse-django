from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Doctor, Appointment
from .serializers import DoctorSerializer, AppointmentSerializer


@login_required
def dashboard_view(request):
    appointments = Appointment.objects.filter(patient=request.user).select_related('doctor')
    doctors = Doctor.objects.all()
    return render(request, 'appointments/dashboard.html', {
        'appointments': appointments,
        'doctors': doctors,
        'user': request.user
    })


@login_required
def book_view(request):
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        reason = request.POST.get('reason', '')

        doctor = get_object_or_404(Doctor, id=doctor_id)
        Appointment.objects.create(
            patient=request.user, doctor=doctor,
            date=date, time_slot=time_slot, reason=reason
        )
        messages.success(request, 'Appointment booked successfully!')
        return redirect('/dashboard/')

    return render(request, 'appointments/book.html', {'doctors': doctors})


@login_required
def cancel_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, patient=request.user)
    appt.status = 'cancelled'
    appt.save()
    messages.success(request, 'Appointment cancelled.')
    return redirect('/dashboard/')


# DRF ViewSets
class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # users only see their own appointments
        return Appointment.objects.filter(patient=self.request.user)

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        appt = self.get_object()
        appt.status = 'cancelled'
        appt.save()
        return Response({'status': 'cancelled'})