# Create your models here.
from django.conf import settings
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files import File


USER_TYPE = (
    ('patient', 'Patient'),
    ('hospital', 'Hospital'),
)

class User(AbstractUser):
    user_type = models.CharField(max_length=10, choices=USER_TYPE)

class Appointment(models.Model):
    patient = models.ForeignKey(User, related_name='appointments', on_delete=models.CASCADE, limit_choices_to={'user_type': 'patient'})
    doctor = models.ForeignKey(User, related_name='consultations', on_delete=models.CASCADE, limit_choices_to={'user_type': 'hospital'})
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    meeting_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
class MobileClinicRequest(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 'patient'})
    address = models.TextField()
    symptoms = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    visit_date = models.DateField(null=True, blank=True)
    visit_time = models.TimeField(null=True, blank=True)
    hospital = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mobile_clinic_requests', null=True, blank=True, limit_choices_to={'user_type': 'hospital'})
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_latest_visit_date(self):
        return self.requested_at.date() + timedelta(days=3)

# --------------------------------------------------------------------------------

# class TreatmentRecord(models.Model):
#     patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 'patient'})
#     hospital = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_records', limit_choices_to={'user_type': 'hospital'})
#     description = models.TextField()
#     document = models.FileField(upload_to='treatment_documents/')
#     created_at = models.DateTimeField(auto_now_add=True)

class TreatmentRecord(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'patient'}
    )
    hospital = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_records',
        limit_choices_to={'user_type': 'hospital'}
    )
    description = models.TextField()
    document = models.FileField(upload_to='treatment_documents/')
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ Add this field to allow patients to control visibility
    is_visible_to_others = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.patient.username} - {self.description[:20]}"


class QRAccessControl(models.Model):
    patient = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 'patient'})
    allow_access = models.BooleanField(default=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def save(self, *args, **kwargs):
        qr_data = f"http://127.0.0.1:8000/qr-access/{self.patient.id}/"
        qr_image = qrcode.make(qr_data)
        buffer = BytesIO()
        qr_image.save(buffer)
        self.qr_code.save(f'qr_{self.patient.id}.png', File(buffer), save=False)
        super().save(*args, **kwargs)

class TreatmentFile(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='treatment_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_visible_to_other_hospitals = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient.username}'s Treatment File - {self.uploaded_at.strftime('%Y-%m-%d')}"