from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('hospital', 'Hospital'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Hospital(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=20)
    total_beds = models.PositiveIntegerField()
    # available_beds = models.PositiveIntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
    
    @property
    def available_beds(self):
        admitted_count = Patient.objects.filter(hospital=self).count()
        return self.total_beds - admitted_count
# Create your models here.

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
