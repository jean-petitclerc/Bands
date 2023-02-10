from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Country, Genre
from .forms import FormAjoutGenre, FormConfirmation

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
        raise Http404("Le Genre n'a pas été retrouvé.")
    return render(request,
                  'bands/genre/detail.html',
                  {'genre': genre})


@login_required
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


@login_required
def supprimer_genre(request, id):
    if request.method == 'GET':
        try:
            genre = Genre.objects.get(id=id)
            return render(request, 'bands/genre/supp.html',
                      {'form':FormConfirmation, 'genre': genre})
        except Genre.DoesNotExist:
            raise Http404("Le Genre n'a pas été retrouvé.")
    else:
        try:
            form = FormConfirmation(request.POST)
            genre = Genre.objects.get(id=id)
            genre.delete()
            return redirect('bands:list_genres')
        except Genre.DoesNotExist:
            raise Http404("Le Genre n'a pas été retrouvé.")
        except ValueError:
            return render(request, 'bands/genre/supp.html',
                          {'form':FormSuppGenre(), 'error':'Données invalide.'})

def home(request):
    return render(request, 'index.html')
