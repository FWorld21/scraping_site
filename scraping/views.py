from django.core.paginator import Paginator
from django.shortcuts import render
from . models import Vacancy
from . forms import FormForSearch


# Create your views here.
def home(request):
    form = FormForSearch()
    return render(request, "scraping/home.html", {"form": form})


def list_view(request):
    form = FormForSearch()
    city = request.GET.get("city")
    lang = request.GET.get("lang")
    page_obj = []
    context = {'city': city, 'lang':lang, 'form': form}
    if city or lang:
        _filter = {}
        if city:
            _filter["city__slug"] = city
        if lang:
            _filter["language__slug"] = lang
        vacancies = Vacancy.objects.filter(**_filter)
        paginator = Paginator(vacancies, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, "scraping/list.html", context)
