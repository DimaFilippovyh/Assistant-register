from django import forms
from .models import Doctor, Patient, Entry


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'category', 'photo']
        labels = {'first_name': 'First name', 'last_name': 'Last name',
            'category': 'Category', 'photo': 'Photo'}


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'polis']
        labels = {'first_name': '', 'last_name': '', 'polis': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['date_time', 'price']
        labels = {'date_time': '', 'price': ''}
        # widgets = {
        #     'date_time': forms.SelectDateWidget()  # TODO:
        # }
