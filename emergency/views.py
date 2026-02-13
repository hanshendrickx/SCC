from django.shortcuts import render


def start(request):
    return render(request, "emergency/start.html")


def threat(request):
    # Add your threat response logic here
    return render(request, "emergency/threat.html")
