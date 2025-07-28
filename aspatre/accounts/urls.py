from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.home, name='home'),         
    path('page1/', views.page1_view, name='page1'),
    path('ab1/', views.ab1, name='ab1'),
    path('ab2/', views.ab2, name='ab2'),
    path('ab3/', views.ab3, name='ab3')
]
