from django import forms
from .models import Hospital, User
from django.contrib.auth.forms import UserCreationForm

class BedUpdateForm(forms.ModelForm):
    class Meta:
        model = Hospital
        # fields = ['total_beds', 'available_beds', 'latitude', 'longitude']
        fields = ['name', 'address', 'contact', 'total_beds']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')