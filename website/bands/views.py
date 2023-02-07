from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .models import Country, Genre
from .forms import FormAjoutGenre

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


def ajout_genre(request):
    if request.method == 'GET':
        return render(request, 'bands/genre/ajout.html',
                      {'form':FormAjoutGenre})
    else:
        try:
            form = FormAjoutGenre(request.POST)
            genre = form.save(commit=False)
            genre.aud_crt_user = request.user
            genre.save()
            return redirect('bands:list_genres')
        except ValueError:
            return render(request, 'bands/genre/ajout.html',
                          {'form':FormAjoutGenre(), 'error':'Données invalide.'})


def home(request):
    return render(request, 'index.html')
