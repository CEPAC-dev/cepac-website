from django.shortcuts import render

def home(request):
    return render(request, "main/index.html")

def about(request):
    return render(request, "about/index.html")

def contact(request):
    return render(request, "contact/index.html")

def portfolio(request):
    return render(request, "portfolio/index.html")

def team(request):
    return render(request, "team/index.html")
def services(request):
    return render(request, "services/index.html")
