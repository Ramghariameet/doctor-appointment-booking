from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *

def landingPage (request) :

    return render(request, "landing_page.html")



def registerPage(request):
    return render(request, 'register.html')

def dashboard(request):
    context = {
        "doctors" : [] , "appointments" : [], 
        "name": request.user.username
    }

    all_doctors = Doctor.objects.all()
    for doctor in all_doctors:
        temp = {
            "name" : doctor.userId.username,
        }
        context["doctors"].append(temp)
    all_appointments = Appointment.objects.filter(docId__userId_id = request.user.id)
    for appointment in all_appointments:
        temp = {
            # "doctor_name" : f"{appointment.docId.userId.first_name} {appointment.docId.userId.last_name}"
            "doctor_name" : f"{appointment.docId.userId.username}",
            "date": appointment.date,
            "reason": appointment.reason,
            "patient_name": appointment.name,
            "patient_age" : appointment.age,
            "patient_gender" : appointment.gender,
            "patient_email" : appointment.email,
            "patient_phone" : appointment.phone_number
        }
        context['appointments'].append(temp)
    return render(request, "dashboard.html", context)

def dashboardpatient(request):
    currentUser = request.user
    context = {
        "doctors": [],
        "name": request.user.username
    }

    doctors = Doctor.objects.all()
    i=1
    for doctor in doctors:
        temp = {
            "id": i,
            "name": doctor.userId.username
        }
        i+=1
        context["doctors"].append(temp)

    appointments_user = Appointment.objects.filter(userId=currentUser)
    appointments=[]
    for appointment in appointments_user:
        print(appointment)
        temp = {
            "patient_name" : appointment.name,
            "date" : appointment.date,
            "gender": appointment.gender,
            "age": appointment.age,
            "doctor_name": appointment.docId.userId.username
        }
        appointments.append(temp)
    
    context["appointments"] = appointments
    return render(request, 'dashboardpatient.html', context)

def booking(request):
    return render(request, "booking.html")

def Appointmentdetail(request):
    return render(request, 'Appointmentdetail.html')

def Appointments(request):
    Doctors = Doctor.objects.filter(userId = request.user.id)
    if len(Doctors)> 0:
        all_appointments = Appointment.objects.filter(docId=Doctors[0])
    else:
        all_appointments = Appointment.objects.filter(userId = request.user.id)
    context = {
        "appointments" : []
    }

    for appointment in all_appointments:
        temp = {
            # "doctor_name" : f"{appointment.docId.userId.first_name} {appointment.docId.userId.last_name}"
            "doctor_name" : f"{appointment.docId.userId.username}",
            "date": appointment.date,
            "reason": appointment.reason,
            "patient_name": appointment.name,
            "patient_age" : appointment.age,
            "patient_gender" : appointment.gender,
            "patient_email" : appointment.email,
            "patient_phone" : appointment.phone_number
        }
        context['appointments'].append(temp)

    print(context)
    return render(request, 'Appointments.html', context)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('register_username')
            email = data.get('register_email')
            password = data.get('register_password')
            print(data)

            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return JsonResponse({'success': True})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        username = data.get('login_username')
        password = data.get('login_password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            Doctors = Doctor.objects.filter(userId = request.user.id)
            if len(Doctors)> 0:
                return JsonResponse({'success': True, 'redirect': '/dashboard'})
            else:
                return JsonResponse({'success': True, 'redirect': '/dashboardpatient'})
            
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})