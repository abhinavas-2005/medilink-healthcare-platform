from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Hospital,Patient
from .forms import BedUpdateForm, CustomUserCreationForm
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.http import require_POST
from django.utils.safestring import mark_safe

class CustomLoginView(LoginView):
    template_name = 'login.html'

# class CustomLogoutView(LogoutView):
#     pass
def CustomLogoutView(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.role == 'hospital':
                Hospital.objects.create(
                    name='Hospital Name',
                    address='Address',
                    contact='1234567890',
                    latitude=0.0,
                    longitude=0.0,
                    total_beds=0,
                    admin=user
                )
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# @login_required
# def dashboard(request):
#     if request.user.role == 'hospital':
#         hospital = request.user.hospital
#         form = BedUpdateForm(instance=hospital)
#         if request.method == 'POST':
#             form = BedUpdateForm(request.POST, instance=hospital)
#             if form.is_valid():
#                 form.save()
#                 return redirect('dashboard')
#         return render(request, 'hospital_dashboard.html', {'form': form})
#     else:
#         hospitals = Hospital.objects.filter(available_beds__gt=0)
#         return render(request, 'user_dashboard.html', {'hospitals': hospitals})

# @login_required
# def dashboard(request):
#     if request.user.role == 'hospital':
#         hospital = request.user.hospital
#         form = BedUpdateForm(instance=hospital)
#         if request.method == 'POST':
#             form = BedUpdateForm(request.POST, instance=hospital)
#             if form.is_valid():
#                 form.save()
#                 return redirect('dashboard')
#         return render(request, 'hospital_dashboard.html', {'form': form})
#     else:
#         # You can't filter on 'available_beds' as it's a Python property
#         hospitals = [h for h in Hospital.objects.all() if h.available_beds > 0]
#         return render(request, 'user_dashboard.html', {'hospitals': hospitals})

# views.py
from django.core.serializers.json import DjangoJSONEncoder
import json

@login_required
def dashboard(request):
    if request.user.role == 'hospital':
        hospital = request.user.hospital
        form = BedUpdateForm(instance=hospital)
        if request.method == 'POST':
            form = BedUpdateForm(request.POST, instance=hospital)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        return render(request, 'hospital_dashboard.html', {'form': form})
    else:
        hospitals = [h for h in Hospital.objects.all() if h.available_beds > 0]

        # Prepare list of hospital dicts for geocoding in JS
        hospital_data = [
            {
                'name': h.name,
                'address': h.address,
                'available_beds': h.available_beds
            }
            for h in hospitals
        ]
        return render(request, 'user_dashboard.html', {
            'hospitals': hospitals,
            'hospital_data_json': mark_safe(json.dumps(hospital_data, cls=DjangoJSONEncoder))
        })


# @login_required
# def admit_patient(request, hospital_id):
#     hospital = Hospital.objects.get(id=hospital_id)
#     if request.user.role == 'user':
#         # Avoid duplicate admissions
#         if not hasattr(request.user, 'patient'):
#             Patient.objects.create(user=request.user, hospital=hospital)
#     return redirect('dashboard')
@login_required
@require_POST
def admit_patient(request, hospital_id):
    if request.user.role != 'user':
        return redirect('dashboard')

    hospital = get_object_or_404(Hospital, id=hospital_id)

    # Avoid duplicate admissions
    if not hasattr(request.user, 'patient'):
        Patient.objects.create(user=request.user, hospital=hospital)

    return redirect('dashboard')

