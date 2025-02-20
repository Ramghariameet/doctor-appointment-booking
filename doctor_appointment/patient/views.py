from django.shortcuts import render

def landingPage (request) :
    return render(request, "landing_page.html")



def registerPage(request):
    return render(request, 'register.html')

def dashboard(request):
    return render(request, "dashboard.html")