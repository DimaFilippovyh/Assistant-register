from django import forms
from .models import Doctor, Patient, Entry


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'category', 'photo']
        labels = {'first_name': 'First name', 'last_name': 'Last name', 'category': 'Category', 'photo': 'Photo'}


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'polis']
        labels = {'first_name': 'First name', 'last_name': 'Last name', 'Polis': 'polis'}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['patient', 'price']
        labels = {'patient': 'Patient', 'price': 'Price'}
