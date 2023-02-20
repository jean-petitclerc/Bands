from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Band, BandLink, Country, Genre
from .forms import FormAjoutGenre, FormModifGenre, FormAjoutBand, FormModifBand, FormAjoutBandLink, FormConfirmation


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
                          {'form':FormAjoutGenre(), 'error':'Données invalides.'})


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
                          {'form':FormConfirmation(), 'error':'Données invalides.'})


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
            genre.save()
            return redirect('bands:list_genres')
        except ValueError:
            return render(request, 'bands/genre/modif.html',
                          {'form':form, 'error':'Données invalides.'})


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


@login_required
def ajout_band(request):
    if request.method == 'GET':
        return render(request, 'bands/band/ajout.html',
                      {'form':FormAjoutBand})
    else:
        try:
            form = FormAjoutBand(request.POST)
            band = form.save(commit=False)
            band.aud_crt_user = request.user
            band.save()
            return redirect('bands:list_bands')
        except ValueError:
            return render(request, 'bands/band/ajout.html',
                          {'form':FormAjoutBand(), 'error':'Données invalides.'})


@login_required
def supprimer_band(request, id):
    if request.method == 'GET':
        try:
            band = Band.objects.get(id=id)
            return render(request, 'bands/band/supp.html',
                      {'form':FormConfirmation, 'band': band})
        except Band.DoesNotExist:
            raise Http404("Le band n'a pas été retrouvé.")
    else:
        try:
            form = FormConfirmation(request.POST)
            band = Band.objects.get(id=id)
            band.delete()
            return redirect('bands:list_bands')
        except Band.DoesNotExist:
            raise Http404("Le band n'a pas été retrouvé.")
        except ValueError:
            return render(request, 'bands/band/supp.html',
                          {'form':FormConfirmation(), 'error':'Données invalides.'})


@login_required
def modifier_band(request, id):
    band = get_object_or_404(Band, id=id)
    links = BandLink.objects.filter(band = band)
    if request.method == 'GET':
        form = FormModifBand(instance=band)
        return render(request, 'bands/band/modif.html',
                      {'form':form, 'band': band, 'links': links})
    else:
        try:
            form = FormModifBand(request.POST, instance=band)
            band = form.save(commit=False)
            print(request.user)
            band.aud_upd_user = request.user
            band.save()
            return redirect('bands:list_bands')
        except ValueError:
            return render(request, 'bands/band/modif.html',
                          {'form':form, 'band': band, 'links': links, 'error':'Données invalides.'})


@login_required
def ajout_bandlink(request, band_id):
    band = get_object_or_404(Band,id=band_id)
    if request.method == 'GET':
        return render(request, 'bands/bandlink/ajout.html',
                      {'form':FormAjoutBandLink(), 'band': band})
    else:
        try:
            form = FormAjoutBandLink(request.POST)
            bandlink = form.save(commit=False)
            bandlink.aud_ctr_user = request.user
            bandlink.band = band
            bandlink.save()
            return redirect('bands:detail_band', bandlink.band.id)
        except ValueError:
            return render(request, 'bands/bandlink/ajout.html',
                          {'form': FormAjoutBandLink(), 'band': band, 'error': 'Données invalides.'})
