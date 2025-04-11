from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    speciality = models.TextField(max_length=255)
    fee = models.IntegerField()

class Appointment(models.Model):
    docId = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField(max_length=550)
    age = models.IntegerField()
    name = models.TextField()
    gender = models.TextField()
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=15)
