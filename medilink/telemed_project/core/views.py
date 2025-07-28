import base64
from datetime import timedelta
import io
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone 
# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
import qrcode
from .models import Appointment, TreatmentFile, User, MobileClinicRequest, TreatmentRecord, QRAccessControl
from .forms import AppointmentForm, MobileClinicApprovalForm, MobileClinicRequestForm,TreatmentUploadForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
import uuid
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
#---------------------------------------------------------------------------------------
from django.core.mail import send_mail

User = get_user_model()


# @login_required
# def dashboard(request):
#     if request.user.user_type == 'patient':
#         appointments = Appointment.objects.filter(patient=request.user)
#         return render(request, 'core/patient_dashboard.html', {'appointments': appointments})
#     else:
#         appointments = Appointment.objects.filter(doctor=request.user)
#         return render(request, 'core/doctor_dashboard.html', {'appointments': appointments})

from .models import Appointment, MobileClinicRequest  # Make sure this is imported

@login_required
def dashboard(request):
    if request.user.user_type == 'patient':
        appointments = Appointment.objects.filter(patient=request.user)
        my_requests = MobileClinicRequest.objects.filter(patient=request.user).order_by('-requested_at')
        return render(request, 'core/patient_dashboard.html', {
            'appointments': appointments,
            'my_requests': my_requests
        })
    else:
        appointments = Appointment.objects.filter(doctor=request.user)
        return render(request, 'core/doctor_dashboard.html', {'appointments': appointments})


@login_required
def book_appointment(request):
    if request.user.user_type != 'patient':
        return redirect('dashboard')
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect('dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'core/book_appointment.html', {'form': form})

# @login_required
# def update_appointment_status(request, appointment_id, status):
#     appointment = Appointment.objects.get(id=appointment_id)
#     if request.user != appointment.doctor:
#         return redirect('dashboard')
#     appointment.status = status
#     if status == 'Approved':
#         appointment.meeting_link = "https://meet.example.com/" + str(appointment.id)
#     appointment.save()
#     return redirect('dashboard')


@login_required
def update_appointment_status(request, appointment_id, status):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.user != appointment.doctor:
        return redirect('dashboard')
    
    appointment.status = status
    
    if status == 'Approved' and not appointment.meeting_link:
        # Use a secure, unique meeting ID
        unique_id = str(uuid.uuid4())
        appointment.meeting_link = f"https://meet.jit.si/{unique_id}"
    
    appointment.save()
    return redirect('dashboard')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def home(request):
    return render(request, 'core/home.html')  # optional landing page

# ------------------------------------------------------------------------------------------------------------------------

@login_required
def book_mobile_clinic(request):
    if request.user.user_type != 'patient':
        return redirect('dashboard')
    if request.method == 'POST':
        form = MobileClinicRequestForm(request.POST)
        if form.is_valid():
            mobile_clinic = form.save(commit=False)
            mobile_clinic.patient = request.user
            mobile_clinic.status = 'Pending'
            mobile_clinic.save()
            return redirect('dashboard')
    else:
        form = MobileClinicRequestForm()
    return render(request, 'core/book_mobile_clinic.html', {'form': form})

@login_required
def manage_mobile_clinic_requests(request):
    if request.user.user_type != 'hospital':
        return redirect('dashboard')

    pending_requests = MobileClinicRequest.objects.filter(status='Pending')
    approved_requests = MobileClinicRequest.objects.filter(status='Approved')

    return render(request, 'core/manage_mobile_clinic.html', {
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
    })
    # if request.user.user_type != 'hospital':
    #     return redirect('dashboard')
    # requests = MobileClinicRequest.objects.filter(status='Pending')
    # return render(request, 'core/manage_mobile_clinic.html', {'requests': requests})

# @login_required
# def update_mobile_clinic_status(request, request_id, status):
#     clinic_request = get_object_or_404(MobileClinicRequest, id=request_id)
#     if request.user.user_type != 'hospital':
#         return redirect('dashboard')

#     clinic_request.status = status
#     if status == 'Approved':
#         clinic_request.hospital = request.user
#         clinic_request.visit_date = timezone.now().date() + timedelta(days=2)  # example: 2 days later
#         clinic_request.visit_time = timezone.now().time().replace(second=0, microsecond=0)
#         # Optionally send email
#         send_mail(
#             subject="Mobile Clinic Visit Approved",
#             message=f"Your mobile clinic visit has been scheduled for {clinic_request.visit_date} at {clinic_request.visit_time}.",
#             from_email="admin@telemed.com",
#             recipient_list=[clinic_request.patient.email],
#             fail_silently=True
#         )
#     clinic_request.save()
#     return redirect('manage_mobile_clinic')

# @login_required
# def update_mobile_clinic_status(request, request_id, status):
#     clinic_request = get_object_or_404(MobileClinicRequest, id=request_id)

#     if request.user.user_type != 'hospital':
#         return redirect('dashboard')

#     if status == 'Approved':
#         if request.method == 'POST':
#             form = MobileClinicApprovalForm(request.POST, instance=clinic_request)
#             if form.is_valid():
#                 clinic_request = form.save(commit=False)
#                 clinic_request.status = 'Approved'
#                 clinic_request.hospital = request.user

#                 # Email logic
#                 send_mail(
#                     subject="Mobile Clinic Visit Approved",
#                     message=f"Your mobile clinic visit has been scheduled for {clinic_request.visit_date} at {clinic_request.visit_time}.",
#                     from_email="admin@telemed.com",
#                     # recipient_list=[clinic_request.patient.email],
#                     recipient_list=['kashwitmkashwi@gmail.com'],
#                     fail_silently=True
#                 )

#                 clinic_request.save()
#                 return redirect('manage_mobile_clinic')
#         else:
#             form = MobileClinicApprovalForm(instance=clinic_request)
#         return render(request, 'core/approve_mobile_clinic.html', {
#             'form': form,
#             'clinic_request': clinic_request
#         })

#     elif status == 'Rejected':
#         clinic_request.status = 'Rejected'
#         clinic_request.save()
#         return redirect('manage_mobile_clinic')

@login_required
def update_mobile_clinic_status(request, request_id, status):
    clinic_request = get_object_or_404(MobileClinicRequest, id=request_id)

    if request.user.user_type != 'hospital':
        return redirect('dashboard')

    if status == 'Approved' and request.method == 'POST':
        visit_date = request.POST.get('visit_date')
        visit_time = request.POST.get('visit_time')

        if visit_date and visit_time:
            clinic_request.status = 'Approved'
            clinic_request.hospital = request.user
            clinic_request.visit_date = visit_date
            clinic_request.visit_time = visit_time

            # Email logic
            send_mail(
                subject="Mobile Clinic Visit Approved",
                message=f"Your mobile clinic visit has been scheduled for {visit_date} at {visit_time}.",
                from_email="admin@telemed.com",
                recipient_list=[clinic_request.patient.email],
                fail_silently=True
            )

            clinic_request.save()

    elif status == 'Rejected':
        clinic_request.status = 'Rejected'
        clinic_request.save()

    return redirect('manage_mobile_clinic')

    
@login_required
def approve_mobile_clinic(request, request_id):
    clinic_request = get_object_or_404(MobileClinicRequest, id=request_id, status='Pending')

    if request.user.user_type != 'hospital':
        return redirect('dashboard')

    if request.method == 'POST':
        form = MobileClinicApprovalForm(request.POST, instance=clinic_request)
        if form.is_valid():
            approved = form.save(commit=False)
            approved.status = 'Approved'
            approved.hospital = request.user
            approved.save()

            send_mail(
                subject="Mobile Clinic Visit Approved",
                message=f"Your mobile clinic visit is scheduled for {approved.visit_date} at {approved.visit_time}.",
                from_email="admin@telemed.com",
                recipient_list=[approved.patient.email],
                fail_silently=True
            )
            return redirect('manage_mobile_clinic')
    else:
        form = MobileClinicApprovalForm(instance=clinic_request)

    return render(request, 'core/approve_mobile_clinic.html', {'form': form, 'clinic_request': clinic_request})


# ------------------------------------------------------------------

# @login_required
# def upload_treatment_file(request, patient_id):
#     if request.user.user_type != 'hospital':
#         return HttpResponseForbidden()

#     patient = get_object_or_404(settings.AUTH_USER_MODEL, id=patient_id, user_type='patient')
#     if request.method == 'POST':
#         form = TreatmentUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             record = form.save(commit=False)
#             record.patient = patient
#             record.hospital = request.user
#             record.save()
#             return redirect('dashboard')
#     else:
#         form = TreatmentUploadForm()
#     return render(request, 'core/upload_treatment_file.html', {'form': form, 'patient': patient})

# @login_required
# def upload_treatment_file(request, patient_id):
#     if request.user.user_type != 'hospital':
#         return HttpResponseForbidden()

#     patient = get_object_or_404(User, id=patient_id, user_type='patient')

#     if request.method == 'POST':
#         form = TreatmentUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             record = form.save(commit=False)
#             record.patient = patient
#             record.hospital = request.user
#             record.save()
#             return redirect('dashboard')
#     else:
#         form = TreatmentUploadForm()

#     return render(request, 'core/upload_treatment_file.html', {'form': form, 'patient': patient})

# @login_required
# def upload_treatment_file(request):
#     if request.user.user_type != 'hospital':
#         return HttpResponseForbidden()

#     if request.method == 'POST':
#         form = TreatmentUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             record = form.save(commit=False)
#             record.hospital = request.user
#             record.save()
#             return redirect('dashboard')
#     else:
#         form = TreatmentUploadForm()

#     return render(request, 'core/upload_treatment_file.html', {'form': form})

@login_required
def upload_treatment_file(request):
    if request.user.user_type != 'hospital':
        return HttpResponseForbidden("Only hospital users can upload files.")

    if request.method == 'POST':
        form = TreatmentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            treatment = form.save(commit=False)
            treatment.hospital = request.user
            treatment.save()
            return redirect('dashboard')
    else:
        form = TreatmentUploadForm()

    return render(request, 'core/upload_treatment_file.html', {'form': form})


# @login_required
# def view_my_treatment_files(request):
#     records = TreatmentRecord.objects.filter(patient=request.user)
#     qr_info = QRAccessControl.objects.get_or_create(patient=request.user)[0]
#     return render(request, 'core/my_treatment_files.html', {'records': records, 'qr_info': qr_info})
@login_required
def view_my_treatment_files(request):
    if request.user.user_type != 'patient':
        return HttpResponseForbidden()

    treatment_files = TreatmentRecord.objects.filter(patient=request.user)

    qr_code_base64 = None
    if treatment_files.exists():
        # Generate QR linking to scan view for this patient
        qr = qrcode.make(request.build_absolute_uri(
            reverse('qr_access', args=[request.user.id])
        ))
        buffer = io.BytesIO()
        qr.save(buffer, format='PNG')
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'core/my_treatment_files.html', {
        'treatment_files': treatment_files,
        'qr_code_base64': qr_code_base64,
    })


# @login_required
# def toggle_qr_access(request):
#     qr_info, created = QRAccessControl.objects.get_or_create(patient=request.user)
#     qr_info.allow_access = not qr_info.allow_access
#     qr_info.save()
#     return redirect('view_my_treatment_files')

from django.views.decorators.http import require_POST

@require_POST
@login_required
def toggle_qr_access(request):
    if request.user.user_type != 'patient':
        return HttpResponseForbidden()

    file_id = request.POST.get('file_id')
    try:
        record = TreatmentRecord.objects.get(id=file_id, patient=request.user)
        record.is_visible_to_others = not record.is_visible_to_others
        record.save()
    except TreatmentRecord.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to modify this file.")

    return redirect('view_my_treatment_files')



# def qr_access_view(request, patient_id):
#     access_info = get_object_or_404(QRAccessControl, patient_id=patient_id)
#     if access_info.allow_access:
#         records = TreatmentRecord.objects.filter(patient=access_info.patient)
#         return render(request, 'core/qr_view_treatment_files.html', {'records': records})
#     else:
#         return render(request, 'core/access_denied.html')

@require_POST
def qr_access_view(request, patient_id): 
    access_info = get_object_or_404(QRAccessControl, patient_id=patient_id)
    if access_info.allow_access:
        records = TreatmentRecord.objects.filter(patient=access_info.patient, is_visible_to_others=True)
        return render(request, 'core/qr_view_treatment_files.html', {'records': records})
    else:
        return render(request, 'core/access_denied.html')

# @login_required
# def scan_qr_view(request):
#     treatment_file = None
#     if request.user.user_type != 'hospital':
#         return redirect('dashboard')

#     if request.method == 'POST':
#         token = request.POST.get('qr_token')
#         treatment_file = get_object_or_404(TreatmentFile, qr_token=token, visible_to_others=True)

#     return render(request, 'core/scan_qr_view.html', {'treatment_file': treatment_file})




# @csrf_exempt
# @login_required
# def scan_qr_view(request):
#     if request.user.user_type != 'hospital':
#         return redirect('dashboard')

#     if request.method == 'POST':
#         qr_data = request.POST.get('qr_data')  # This is the full URL from the QR code

#         if qr_data and qr_data.startswith('http://127.0.0.1:8000/qr-access/'):
#             return redirect(qr_data)
#         else:
#             return HttpResponse("Invalid QR code.", status=400)

#     return render(request, 'core/scan_qr_view.html')

from urllib.parse import urlparse

# @login_required
# def scan_qr_view(request):
#     records = None
#     if request.user.user_type != 'hospital':
#         return redirect('dashboard')

#     if request.method == 'POST':
#         qr_data = request.POST.get('qr_token')  # This is the full URL

#         try:
#             # Extract patient_id from the URL like http://127.0.0.1:8000/qr-access/5/
#             path = urlparse(qr_data).path
#             if path.startswith('/qr-access/'):
#                 patient_id = int(path.split('/')[-2]) if path.endswith('/') else int(path.split('/')[-1])
                
#                 access_info = QRAccessControl.objects.get(patient_id=patient_id)
#                 if access_info.allow_access:
#                     records = TreatmentRecord.objects.filter(patient_id=patient_id, is_visible_to_others=True)
#         except Exception as e:
#             print("QR scan error:", e)

#     return render(request, 'core/scan_qr_view.html', {'records': records})
# @login_required
# def scan_qr_view(request):
#     records = None

#     # Only hospital can access this view
#     if request.user.user_type != 'hospital':
#         return redirect('dashboard')

#     if request.method == 'POST':
#         qr_data = request.POST.get('qr_token')  # Full scanned QR URL
#         try:
#             path = urlparse(qr_data).path  # Example: /qr-access/5/
#             parts = path.strip('/').split('/')
            
#             if len(parts) == 2 and parts[0] == 'qr-access':
#                 patient_id = int(parts[1])  # safely extract the patient ID

#                 access_info = get_object_or_404(QRAccessControl, patient_id=patient_id)
                
#                 if access_info.allow_access:
#                     records = TreatmentRecord.objects.filter(
#                         patient_id=patient_id,
#                         is_visible_to_others=True
#                     )
#                 else:
#                     return render(request, 'core/access_denied.html')

#         except Exception as e:
#             print("QR scan error:", e)
#             return render(request, 'core/access_denied.html')

#     return render(request, 'core/scan_qr_view.html', {'records': records})

from urllib.parse import urlparse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import TreatmentRecord, QRAccessControl

@login_required
def scan_qr_view(request):
    records = None
    access_denied = False  # <- for template logic

    if request.user.user_type != 'hospital':
        return redirect('dashboard')

    if request.method == 'POST':
        qr_data = request.POST.get('qr_token')
        print("Scanned QR data:", qr_data)

        try:
            path = urlparse(qr_data).path
            parts = path.strip('/').split('/')

            if len(parts) == 2 and parts[0] == 'qr-access':
                patient_id = int(parts[1])

                access_info = get_object_or_404(QRAccessControl, patient_id=patient_id)

                if access_info.allow_access:
                    records = TreatmentRecord.objects.filter(
                        patient_id=patient_id,
                        is_visible_to_others=True
                    )
                else:
                    access_denied = True
            else:
                access_denied = True
        except Exception as e:
            print("QR scan error:", e)
            access_denied = True

    return render(request, 'core/scan_qr_view.html', {
        'records': records,
        'access_denied': access_denied
    })

# # views.py
# @login_required
# def qr_access_view(request, patient_id): 
#     access_info = get_object_or_404(QRAccessControl, patient_id=patient_id)
#     if access_info.allow_access:
#         records = TreatmentRecord.objects.filter(patient=access_info.patient)
#         return render(request, 'core/qr_view_treatment_files.html', {'records': records})
#     else:
#         return render(request, 'core/access_denied.html')
