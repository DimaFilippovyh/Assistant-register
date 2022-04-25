import calendar
from datetime import datetime, time
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Doctor, Patient, Entry
from .forms import DoctorForm, EntryForm, PatientForm


def index(request):
    return render(request, 'assistant_register/index.html')


def doctors(request):
    doctors = Doctor.objects.order_by('category')
    context = {'doctors': doctors}

    return render(request, 'assistant_register/doctors.html', context=context)


@login_required
def doctor(request, doctor_id):
    today = datetime.now()
    today_year, today_month = today.year, today.month
    start_date = today.replace(day=1, hour=0, minute=0, second=0)
    end_date = today.replace(day=calendar.monthrange(today_year, today_month)[1], hour=0, minute=0, second=0)

    doctor = Doctor.objects.get(id=doctor_id)
    entries = (doctor.entry_set.annotate(date=TruncDate('date_time'))
               .filter(date_time__range=(start_date, end_date))
               .values('date')
               .annotate(count=Count('date'))
               .order_by())

    entries = [i['date'] for i in entries if i['count'] == 4]
    print(entries)
    lst_days = []

    obj = calendar.Calendar()
    temp_lst = list(obj.itermonthdates(2022, 4))

    for i in temp_lst:
        # -1 выходные 0 занято none свободно
        if i.month != today_month:
            flag = -1
        elif datetime.weekday(i) in (5, 6):
            flag = -1
        elif i in entries:
            flag = 0
        else:
            flag = None

        lst_days.append({'date': i, 'flag': flag})

    lst_days = [lst_days[i:i + 7] for i in range(0, len(lst_days), 7)]

    context = {'doctor': doctor, 'entries': entries, 'lst_days': lst_days}
    return render(request, 'assistant_register/doctor.html', context=context)


@login_required
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


@login_required
def entry_day(request, doctor_id, date):
    doctor = Doctor.objects.get(id=doctor_id)
    entries = (doctor.entry_set.annotate(date=TruncDate('date_time'))
               .values('date_time')
               .filter(date=date))

    entries = [time(i['date_time'].hour) for i in entries]
    temp_lst = [time(hour=i) for i in range(8, 12)]
    lst_times = []

    for i in temp_lst:
        flag = None
        if i in entries:
            flag = 0

        lst_times.append({'time': i, 'hour': i.hour, 'flag': flag})

    context = {'doctor': doctor, 'date': date, 'lst_times': lst_times}
    return render(request, 'assistant_register/entry_day.html', context=context)


@login_required
def entry(request, doctor_id, date, hour):
    doctor = Doctor.objects.get(id=doctor_id)
    today = datetime.combine(date, time(hour))
    entry = Entry.objects.filter(date_time=today, doctor_id=doctor_id)

    if len(entry) == 0:
        if request.method != 'POST':
            form = EntryForm()
        else:
            form = EntryForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                new_entry = form.save(commit=False)
                new_entry.doctor = doctor
                new_entry.date_time = today
                new_entry.save()
                return redirect('assistant_register:entry_day', doctor.id, date)
    else:
        if request.method != 'POST':
            form = EntryForm(instance=entry[0])
        else:
            form = EntryForm(instance=entry[0], data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                return redirect('assistant_register:entry_day', doctor.id, date)

    context = {'doctor': doctor, 'date': date, 'hour': hour, 'form': form}
    return render(request, 'assistant_register/entry.html', context=context)


@login_required
def patients(request):
    patients = Patient.objects.order_by('last_name', 'first_name')
    context = {'patients': patients}

    return render(request, 'assistant_register/patients.html', context=context)


@login_required
def new_patient(request):
    if request.method != 'POST':
        form = PatientForm()
    else:
        form = PatientForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('assistant_register:patients')

    context = {'form': form}
    return render(request, 'assistant_register/new_patient.html', context)
