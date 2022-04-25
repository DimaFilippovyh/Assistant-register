from django.urls import path, register_converter
from . import views
from .path_converter import DateConverter


register_converter(DateConverter, 'date')

app_name = 'assistant_register'
urlpatterns = [
    path('', views.index, name='index'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctor/<int:doctor_id>/', views.doctor, name='doctor'),
    path('new_doctor/', views.new_doctor, name='new_doctor'),
    path('entry_day/<int:doctor_id>/<date:date>/', views.entry_day, name='entry_day'),
    path('entry/<int:doctor_id>/<date:date>/<int:hour>', views.entry, name='entry'),
    path('patients/', views.patients, name='patients'),
    path('new_patient', views.new_patient, name='new_patient')
]
