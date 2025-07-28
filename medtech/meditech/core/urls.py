from django.urls import path
from .views import dashboard, register, CustomLoginView, CustomLogoutView,admit_patient
from django.contrib.auth.decorators import login_required
from .views import dashboard, register, CustomLoginView, CustomLogoutView
from django.contrib.auth.views import LogoutView  # using Django's LogoutView directly

urlpatterns = [
    path('', login_required(dashboard), name='dashboard'),
    path('dashboard/', login_required(dashboard), name='dashboard'),  # Explicit /dashboard route
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView, name='logout'),
    path('admit/<int:hospital_id>/', admit_patient, name='admit'),
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout')
]