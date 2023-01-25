from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Country

def list_countries(request):
    countries = Country.objects.all()
    return render(request,
                 'bands/country/list.html',
                 {'countries': countries})


def detail_country(request, id):
    try:
        country = Country.objects.get(id=id)
    except Country.DoesNotExist:
        raise Http404("No Country found.")
    return render(request,
                  'bands/country/detail.html',
                  {'country': country})


def home(request):
    return render(request, 'index.html')
