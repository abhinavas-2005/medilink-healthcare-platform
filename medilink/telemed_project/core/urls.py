from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('update_status/<int:appointment_id>/<str:status>/', views.update_appointment_status, name='update_status'),
    # urls.py
path('book-mobile-clinic/', views.book_mobile_clinic, name='book_mobile_clinic'),
path('manage-mobile-clinic/', views.manage_mobile_clinic_requests, name='manage_mobile_clinic'),
path('mobile-clinic/update/<int:request_id>/<str:status>/', views.update_mobile_clinic_status, name='update_mobile_clinic_status'),
# path('upload-treatment/<int:patient_id>/', views.upload_treatment_file, name='upload_treatment_file'),
path('upload-treatment/', views.upload_treatment_file, name='upload_treatment_file'),
path('my-treatment-files/', views.view_my_treatment_files, name='view_my_treatment_files'),
path('toggle-access/', views.toggle_qr_access, name='toggle_qr_access'),
path('qr-access/<int:patient_id>/', views.qr_access_view, name='qr_access'),
path('scan-qr/', views.scan_qr_view, name='scan_qr_view'),

] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

