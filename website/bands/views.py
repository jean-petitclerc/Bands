from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import Band, BandAEcouter, BandLink, Country, Genre
from .forms import FormAjoutGenre, FormModifGenre, FormAjoutBand, FormModifBand, FormAjoutBandLink, FormConfirmation
from datetime import datetime as ts

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
    maj_permises = False
    if request.user.is_authenticated:
        if request.user.groups.filter(name = 'Editeur').exists():
            maj_permises = True
    liste_genres = Genre.objects.all()
    paginator = Paginator(liste_genres, 25)
    no_de_page = request.GET.get('page', 1)
    genres = paginator.page(no_de_page)
    return render(request,
                 'bands/genre/list.html',
                 {'genres': genres, 'maj_permises': maj_permises})


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
    if request.user.groups.filter(name = 'Editeur').exists():
        if request.method == 'GET':
            return render(request, 'bands/genre/ajout.html',
                        {'form':FormAjoutGenre})
        else:
            try:
                form = FormAjoutGenre(request.POST)
                genre = form.save(commit=False)
                genre.aud_crt_user = request.user
                genre.save()
                messages.success(request, 'Le genre a été ajouté.')
                return redirect('bands:list_genres')
            except ValueError:
                return render(request, 'bands/genre/ajout.html',
                            {'form':FormAjoutGenre(), 'error':'Données invalides.'})
    else:
        messages.warning(request, "Tu ne peux pas ajouter de genres.")
        return redirect('bands:list_genres')


@login_required
def supprimer_genre(request, id):
    if request.user.groups.filter(name = 'Editeur').exists():
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
                messages.success(request, 'Le genre a été supprimé.')
                return redirect('bands:list_genres')
            except Genre.DoesNotExist:
                raise Http404("Le Genre n'a pas été retrouvé.")
            except ValueError:
                return render(request, 'bands/genre/supp.html',
                            {'form':FormConfirmation(), 'error':'Données invalides.'})
    else:
        messages.warning(request, "Tu ne peux pas supprimer de genres.")
        return redirect('bands:list_genres')


@login_required
def modifier_genre(request, id):
    if request.user.groups.filter(name = 'Editeur').exists():
        genre = get_object_or_404(Genre, id=id)
        if request.method == 'GET':
            form = FormModifGenre(instance=genre)
            return render(request, 'bands/genre/modif.html',
                        {'form':form, 'genre': genre})
        else:
            try:
                form = FormModifGenre(request.POST, instance=genre)
                genre = form.save(commit=False)
                genre.aud_upd_user = request.user
                genre.save()
                messages.success(request, 'Le genre a été modifié.')
                return redirect('bands:list_genres')
            except ValueError:
                return render(request, 'bands/genre/modif.html',
                            {'form':form, 'error':'Données invalides.'})
    else:
        messages.warning(request, "Tu ne peux pas modifier de genres.")
        return redirect('bands:list_genres')


def list_bands(request):
    maj_permises = False
    if request.user.is_authenticated:
        if request.user.groups.filter(name = 'Editeur').exists():
            maj_permises = True
    liste_bands = Band.objects.all()
    if request.user.is_authenticated:
        liste_bands_aimés = request.user.is_fan_of.all()
        liste_bands_à_écouter = BandAEcouter.objects.filter(user = request.user).filter( listened_ts__isnull = True).values_list('band_id', flat=True)
        for b in liste_bands:
            if b in liste_bands_aimés:
                b.is_fan = True
            else:
                b.is_fan = False
            if b.id in liste_bands_à_écouter:
                print("À écouter")
                b.to_listen = True
            else:
                print("Pas à écouter")
                b.to_listen = False
    paginator = Paginator(liste_bands, 25)
    no_de_page = request.GET.get('page', 1)
    bands = paginator.page(no_de_page)
    return render(request,
                 'bands/band/list.html',
                 {'bands': bands, 'maj_permises': maj_permises})


@login_required
def list_my_bands(request):
    maj_permises = False
    if request.user.is_authenticated:
        if request.user.groups.filter(name = 'Editeur').exists():
            maj_permises = True
    liste_bands = request.user.is_fan_of.all()
    for b in liste_bands:
        b.links = BandLink.objects.filter(band = b)
    paginator = Paginator(liste_bands, 25)
    no_de_page = request.GET.get('page', 1)
    bands = paginator.page(no_de_page)
    return render(request,
                 'bands/band/mes_bands.html',
                 {'bands': bands})


def detail_band(request, id, redirect_to):
    try:
        band = Band.objects.get(id=id)
        links = BandLink.objects.filter(band = band)
        genres = band.plays_genres.all()
        countries = band.from_countries.all()
    except Band.DoesNotExist:
        raise Http404("Le Band n'a pas été retrouvé.")
    return render(request,
                  'bands/band/detail.html',
                  {'band': band, 'links': links, 'genres': genres, 'countries': countries, 'redirect_to': redirect_to})


@login_required
def ajout_band(request):
    if request.user.groups.filter(name = 'Editeur').exists():
        if request.method == 'GET':
            return render(request, 'bands/band/ajout.html',
                        {'form':FormAjoutBand})
        else:
            try:
                form = FormAjoutBand(request.POST)
                band = form.save(commit=False)
                band.aud_crt_user = request.user
                band.save()
                messages.success(request, 'Le band a été ajouté.')
                return redirect('bands:list_bands')
            except ValueError:
                messages.error(request, 'Données invalides.')
                return render(request, 'bands/band/ajout.html',
                            {'form':FormAjoutBand(), 'error':'Erreur de validation.'})
    else:
        messages.warning(request, "Tu ne peux pas ajouter de bands.")
        return redirect('bands:list_bands')


@login_required
def supprimer_band(request, id):
    if request.user.groups.filter(name = 'Editeur').exists():
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
                messages.success(request, 'Le band a été supprimé.')
                return redirect('bands:list_bands')
            except Band.DoesNotExist:
                raise Http404("Le band n'a pas été retrouvé.")
            except ValueError:
                return render(request, 'bands/band/supp.html',
                            {'form':FormConfirmation(), 'error':'Données invalides.'})
    else:
        messages.warning(request, "Tu ne peux pas supprimer de bands.")
        return redirect('bands:list_bands')


@login_required
def modifier_band(request, id):
    if request.user.groups.filter(name = 'Editeur').exists():
        band = get_object_or_404(Band, id=id)
        links = BandLink.objects.filter(band = band)
        countries = band.from_countries.all()
        genres = band.plays_genres.all()
        if request.method == 'GET':
            form = FormModifBand(instance=band)
            return render(request, 'bands/band/modif.html',
                        {'form':form, 'band': band, 'links': links, 'countries': countries, 'genres': genres})
        else:
            try:
                form = FormModifBand(request.POST, instance=band)
                band = form.save(commit=False)
                band.aud_upd_user = request.user
                band.save()
                messages.success(request, 'Le band a été modifié.')
                return redirect('bands:list_bands')
            except ValueError:
                return render(request, 'bands/band/modif.html',
                            {'form':form, 'band': band, 'links': links, 'countries': countries, 'genres': genres, 'error':'Données invalides.'})
    else:
        messages.warning(request, "Tu ne peux pas modifier de bands.")
        return redirect('bands:list_bands')


@login_required
def ajout_bandlink(request, band_id):
    if request.user.groups.filter(name = 'Editeur').exists():
        band = get_object_or_404(Band,id=band_id)
        if request.method == 'GET':
            return render(request, 'bands/bandlink/ajout.html',
                        {'form':FormAjoutBandLink(), 'band': band})
        else:
            try:
                form = FormAjoutBandLink(request.POST)
                bandlink = form.save(commit=False)
                bandlink.aud_crt_user = request.user
                bandlink.band = band
                bandlink.save()
                messages.success(request, 'Le lien a été ajouté.')
                return redirect('bands:modifier_band', band_id)
            except ValueError:
                return render(request, 'bands/bandlink/ajout.html',
                            {'form': FormAjoutBandLink(), 'band': band, 'error': 'Données invalides.'})
    else:
        messages.warning(request, "Tu ne peux pas ajouter de liens.")
        return redirect('bands:modifier_band', band_id)


@login_required
def supprimer_bandlink(request, band_id, id):
    if request.user.groups.filter(name = 'Editeur').exists():
        if request.method == 'GET':
            try:
                band = Band.objects.get(id=band_id)
                link = BandLink.objects.get(id=id)
                return render(request, 'bands/bandlink/supp.html',
                        {'form':FormConfirmation, 'band': band, 'link': link})
            except Band.DoesNotExist:
                raise Http404("Le band n'a pas été retrouvé.")
            except BandLink.DoesNotExist:
                raise Http404("Le Lien n'a pas été retrouvé.")
        else:
            try:
                form = FormConfirmation(request.POST)
                band = Band.objects.get(id=band_id)
                link = BandLink.objects.get(id=id)
                link.delete()
                messages.success(request, 'Le lien a été supprimé.')
                return redirect('bands:modifier_band', band_id)
            except Band.DoesNotExist:
                raise Http404("Le band n'a pas été retrouvé.")
            except BandLink.DoesNotExist:
                raise Http404("Le Lien n'a pas été retrouvé.")
    else:
        messages.warning(request, "Tu ne peux pas supprimer de liens.")
        return redirect('bands:modifier_band', band_id)


@login_required
def band_choisir_pays(request, id):
    if request.user.groups.filter(name = 'Editeur').exists():
        try:
            band = Band.objects.get(id=id)
            countries = Country.objects.all().order_by('country_name_fr')
            curr_countries = [c.id for c in band.from_countries.all()]
        except Band.DoesNotExist:
            raise Http404("Le Band n'a pas été retrouvé.")
        return render(request,
                    'bands/band/choisir_pays.html',
                    {'band': band, 'countries': countries, 'curr_countries':  curr_countries})
    else:
        messages.warning(request, "Tu ne peux pas modifier la liste de pays.")
        return redirect('bands:modifier_band', band_id)


@login_required
def band_ajouter_pays(request, band_id, id):
    if request.user.groups.filter(name = 'Editeur').exists():
        try:
            band = Band.objects.get(id=band_id)
            country = Country.objects.get(id=id)
            band.from_countries.add(country)
            band.save()
            return redirect('bands:modifier_band', band_id)
        except Band.DoesNotExist:
            raise Http404("Le Band n'a pas été retrouvé.")
        except Country.DoesNotExist:
            raise Http404("Le Pays n'a pas été retrouvé.")
        return redirect('bands:modifier_band', band_id)
    else:
        messages.warning(request, "Tu ne peux pas modifier la liste de pays.")
        return redirect('bands:modifier_band', band_id)


@login_required
def band_enlever_pays(request, band_id, id):
    if request.user.groups.filter(name = 'Editeur').exists():
        try:
            band = Band.objects.get(id=band_id)
            country = Country.objects.get(id=id)
            band.from_countries.remove(country)
            band.save()
            return redirect('bands:modifier_band', band_id)
        except Band.DoesNotExist:
            raise Http404("Le Band n'a pas été retrouvé.")
        except Country.DoesNotExist:
            raise Http404("Le Pays n'a pas été retrouvé.")
        return redirect('bands:modifier_band', band_id)
    else:
        messages.warning(request, "Tu ne peux pas modifier la liste de pays.")
        return redirect('bands:modifier_band', band_id)


@login_required
def band_choisir_genre(request, id):
    if request.user.groups.filter(name = 'Editeur').exists():
        try:
            band = Band.objects.get(id=id)
            genres = Genre.objects.all().order_by('genre_name')
            curr_genres = [g.id for g in band.plays_genres.all()]
        except Band.DoesNotExist:
            raise Http404("Le Band n'a pas été retrouvé.")
        return render(request,
                    'bands/band/choisir_genre.html',
                    {'band': band, 'genres': genres, 'curr_genres':  curr_genres})
    else:
        messages.warning(request, "Tu ne peux pas modifier la liste de genres.")
        return redirect('bands:modifier_band', band_id)


@login_required
def band_ajouter_genre(request, band_id, id):
    if request.user.groups.filter(name = 'Editeur').exists():
        try:
            band = Band.objects.get(id=band_id)
            genre = Genre.objects.get(id=id)
            band.plays_genres.add(genre)
            band.save()
            return redirect('bands:modifier_band', band_id)
        except Band.DoesNotExist:
            raise Http404("Le Band n'a pas été retrouvé.")
        except Genre.DoesNotExist:
            raise Http404("Le Genre n'a pas été retrouvé.")
        return redirect('bands:modifier_band', band_id)
    else:
        messages.warning(request, "Tu ne peux pas modifier la liste de genres.")
        return redirect('bands:modifier_band', band_id)


@login_required
def band_enlever_genre(request, band_id, id):
    if request.user.groups.filter(name = 'Editeur').exists():
        try:
            band = Band.objects.get(id=band_id)
            genre = Genre.objects.get(id=id)
            band.plays_genres.remove(genre)
            band.save()
            return redirect('bands:modifier_band', band_id)
        except Band.DoesNotExist:
            raise Http404("Le Band n'a pas été retrouvé.")
        except Genre.DoesNotExist:
            raise Http404("Le Genre n'a pas été retrouvé.")
        return redirect('bands:modifier_band', band_id)
    else:
        messages.warning(request, "Tu ne peux pas modifier la liste de genres.")
        return redirect('bands:modifier_band', band_id)


@login_required
def aimer_band(request, id):
    try:
        band = Band.objects.get(id=id)
        request.user.is_fan_of.add(band)
        request.user.save()
        return redirect('bands:list_my_bands')
    except Band.DoesNotExist:
        raise Http404("Le band n'a pas été retrouvé.")


@login_required
def ne_pas_aimer_band(request, id):
    try:
        band = Band.objects.get(id=id)
        request.user.is_fan_of.remove(band)
        request.user.save()
        return redirect('bands:list_my_bands')
    except Band.DoesNotExist:
        raise Http404("Le band n'a pas été retrouvé.")


@login_required
def a_ecouter_band(request, id):
    try:
        band = Band.objects.get(id=id)
        band_à_écouter = BandAEcouter(band=band, user=request.user, listened_ts=None)
        band_à_écouter.save()
        return redirect('bands:list_bands')
    except Band.DoesNotExist:
        raise Http404("Le band n'a pas été retrouvé.")


@login_required
def inscrire_ecoute_band(request, id, redirect_to):
    try:
        print("ID: " + str(id) + " Redirect: " + redirect_to)
        band_à_écouter = BandAEcouter.objects.filter(band_id=id).filter(user_id=request.user).filter(listened_ts__isnull = True).first()
        print(band_à_écouter)
        band_à_écouter.listened_ts = ts.now()
        band_à_écouter.save()
        if redirect_to == "a_ecouter":
            return redirect('bands:liste_a_ecouter')
        else:
            return redirect('bands:list_bands')
    except BandAEcouter.DoesNotExist:
        raise Http404("La demande d'écoute n'a pas été retrouvée.")


@login_required
def liste_a_ecouter(request):
    liste_bands = BandAEcouter.objects.filter(user_id=request.user).filter(listened_ts__isnull = True).order_by('added_ts').all()
    #for b in liste_bands:
    #    b.links = BandLink.objects.filter(band = b).order_by('link_name').all()
    paginator = Paginator(liste_bands, 25)
    no_de_page = request.GET.get('page', 1)
    bands = paginator.page(no_de_page)
    return render(request,
                 'bands/band/a_ecouter.html',
                 {'bands': bands})
