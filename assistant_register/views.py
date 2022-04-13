from django.shortcuts import render, redirect
from .models import Doctor  # , Patient, Entry
from .forms import DoctorForm, EntryForm  # , PatientForm,


def index(request):
    return render(request, 'assistant_register/index.html')


def doctors(request):
    doctors = Doctor.objects.order_by('category')
    context = {'doctors': doctors}

    return render(request, 'assistant_register/doctors.html', context=context)


def doctor(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    entries = doctor.entry_set.order_by('-date_time')
    context = {'doctor': doctor, 'entries': entries}

    return render(request, 'assistant_register/doctor.html', context=context)


def new_doctor(request):
    if request.method != 'POST':
        form = DoctorForm()
    else:
        form = DoctorForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('assistant_register:doctors')

    context = {'form': form}
    return render(request, 'assistant_register/new_doctor.html', context)


def new_entry(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.doctor = doctor
            new_entry.save()
            return redirect('assistant_register:doctor', doctor_id=doctor_id)

    context = {'doctor': doctor, 'form': form}
    return render(request, 'assistant_register/new_entry.html', context)
