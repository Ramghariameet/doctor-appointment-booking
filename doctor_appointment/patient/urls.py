from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingPage),
    path("register", views.registerPage),
    path("dashboard", views.dashboard),
    path("dashboardpatient", views.dashboardpatient),
    path("booking", views.booking),
    path("Appointmentdetail", views.Appointmentdetail),
     path("Appointments", views.Appointments),
    path("api/register", views.register),
    path("api/login", views.login_view),

]