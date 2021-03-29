from django.shortcuts import render
from . models import Vacancy
from . forms import FormForSearch

# Create your views here.
def home(request):
    form = FormForSearch()

    city = request.GET.get("city")
    lang = request.GET.get("lang")
    vacancies = []
    if city or lang:
        _filter = {}
        if city:
            _filter["city__slug"] = city
        if lang:
            _filter["language__slug"] = lang
        vacancies = Vacancy.objects.filter(**_filter)

    return render(request, "scraping/home.html", {"vacancies":vacancies, "form": form})
