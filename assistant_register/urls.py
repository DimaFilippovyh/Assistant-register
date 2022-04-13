from django.urls import path
from . import views


app_name = 'assistant_register'
urlpatterns = [
    path('', views.index, name='index'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctor/<int:doctor_id>/', views.doctor, name='doctor'),
    path('new_doctor/', views.new_doctor, name='new_doctor'),
    path('new_entry/<int:doctor_id>/', views.new_entry, name='new_entry'),
]
