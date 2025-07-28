from django import forms
from .models import Appointment, USER_TYPE ,MobileClinicRequest,TreatmentRecord
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=USER_TYPE)
    class Meta:
        model = User
        fields = ('username', 'email','user_type', 'password1', 'password2')
        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
        
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(user_type='hospital')

class MobileClinicRequestForm(forms.ModelForm):
    class Meta:
        model = MobileClinicRequest
        fields = ['address', 'symptoms']
        
class MobileClinicApprovalForm(forms.ModelForm):
    class Meta:
        model = MobileClinicRequest
        fields = ['visit_date', 'visit_time']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'visit_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

# class TreatmentUploadForm(forms.ModelForm):
#     class Meta:
#         model = TreatmentRecord
#         fields = ['description', 'document']

class TreatmentUploadForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=User.objects.filter(user_type='patient'),
        label="Select Patient",
        required=True
    )

    class Meta:
        model = TreatmentRecord
        fields = ['patient', 'description', 'document']
