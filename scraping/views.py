from django.shortcuts import render
from . models import Vacancy


# Create your views here.
def home(request):
    vacancies = Vacancy.objects.all()
    return render(request, "scraping/home.html", {"vacancies":vacancies})
