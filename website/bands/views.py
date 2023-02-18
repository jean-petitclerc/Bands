from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Band, BandLink, Country, Genre
from .forms import FormAjoutGenre, FormModifGenre, FormConfirmation

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
    liste_genres = Genre.objects.all()
    paginator = Paginator(liste_genres, 25)
    no_de_page = request.GET.get('page', 1)
    genres = paginator.page(no_de_page)
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


@login_required
def modifier_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    if request.method == 'GET':
        form = FormModifGenre(instance=genre)
        return render(request, 'bands/genre/modif.html',
                      {'form':form, 'genre': genre})
    else:
        try:
            form = FormModifGenre(request.POST, instance=genre)
            genre = form.save(commit=False)
            print(request.user)
            genre.aud_upd_user = request.user
            print(genre)
            genre.save()
            return redirect('bands:list_genres')
        except ValueError:
            return render(request, 'bands/genre/modif.html',
                          {'form':form, 'error':'Données invalide.'})


def list_bands(request):
    liste_bands = Band.objects.all()
    paginator = Paginator(liste_bands, 25)
    no_de_page = request.GET.get('page', 1)
    bands = paginator.page(no_de_page)
    return render(request,
                 'bands/band/list.html',
                 {'bands': bands})


def detail_band(request, id):
    try:
        band = Band.objects.get(id=id)
        links = BandLink.objects.filter(band = band)
    except Band.DoesNotExist:
        raise Http404("Le Band n'a pas été retrouvé.")
    return render(request,
                  'bands/band/detail.html',
                  {'band': band, 'links': links})


#def home(request):
#    return render(request, 'index.html')
