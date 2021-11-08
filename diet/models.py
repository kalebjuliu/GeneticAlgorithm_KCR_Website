from django.db import models
from django.contrib.auth.models import User
# Create your models here.

JENIS = (
    ("Lauk Hewani", "Lauk Hewani"),
    ("Lauk Nabati", "Lauk Nabati"),
    ("Sayur", "Sayur"),
    ("Nasi", "Nasi")
)


class Menu(models.Model):
    nama = models.CharField(max_length=250)
    protein = models.FloatField()
    lemak = models.FloatField()
    karbo = models.FloatField()
    kalori = models.FloatField()
    jenis = models.CharField(
        max_length=250,
        choices=JENIS)

    # def __str__(self):
    #     return self.nama, self.kalori, self.jenis


# Daftar Jenis:
# 1. Lauk Hewani
# 2. Lauk Nabati
# 3. Sayur
# 4. Nasi
JENIS_KELAMIN = (
    ("Laki-laki", "Laki-laki"),
    ("Perempuan", "Perempuan"),
)
TINGKAT_AKTIVITAS = (
    ("Sedantary", "Sedentary: little or no exercise"),
    ("Exercise 1-3", "Exercise 1-3 times/week"),
    ("Exercise 4-5", "Exercise 4-5 times/week"),
    ("Daily", "Daily exercise or intense exercise 3-4 times/week"),
    ("Intense", "Intense exercise 6-7 times/week"),
)


class UserBMI(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    umur = models.IntegerField()
    tinggi_badan = models.FloatField()
    berat_badan = models.FloatField()
    jenis_kelamin = models.CharField(
        max_length=100,
        choices=JENIS_KELAMIN)
    tingkat_aktivitas = models.CharField(
        max_length=250,
        choices=TINGKAT_AKTIVITAS)
    bmi = models.FloatField(null=True, blank=True)
    bmr = models.FloatField(null=True, blank=True)
