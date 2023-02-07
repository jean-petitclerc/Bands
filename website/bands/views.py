from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Country, Genre

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


def list_genres(request):
    genres = Genre.objects.all()
    return render(request,
                 'bands/genre/list.html',
                 {'genres': genres})


def detail_genre(request, id):
    try:
        genre = Genre.objects.get(id=id)
    except Genre.DoesNotExist:
        raise Http404("No Genre found.")
    return render(request,
                  'bands/genre/detail.html',
                  {'genre': genre})


def home(request):
    return render(request, 'index.html')
