from django.db import models


class Doctor(models.Model):
    categories = [
        (None, 'Category not selected'),
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
    ]

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    category = models.PositiveSmallIntegerField(("category"),
        choices=categories)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d")

    def __str__(self):
        return f"Доктор: {self.first_name} {self.last_name}"


class Patient(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    polis = models.CharField(max_length=20)

    def __str__(self):
        return f"Пациент: {self.first_name} {self.last_name}"


class Entry(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL,
        blank=True, null=True)
    date_time = models.DateTimeField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        return f"Запись на {self.date_time} с ценой {self.price}"
