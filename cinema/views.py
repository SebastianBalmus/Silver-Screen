from django.shortcuts import render
from django.http import HttpResponse


# Homepage view
def home(request):
    return render(request, 'home.html', {})
