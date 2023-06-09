from django.urls import path
from . import views
#from accounts import views as accounts_views

app_name = 'bands'
urlpatterns = [
    # post views
    path('', views.list_bands, name='list_bands'),
    path('country', views.list_countries, name='list_countries'),
    path('country/<int:id>/', views.detail_country, name='detail_country'),
    path('country_bands/<int:id>/', views.list_country_bands, name='list_country_bands'),
    path('genre', views.list_genres, name='list_genres'),
    path('genre/<int:id>/', views.detail_genre, name='detail_genre'),
    path('genre/ajout', views.ajout_genre, name='ajout_genre'),
    path('genre/supp/<int:id>', views.supprimer_genre, name='supprimer_genre'),
    path('genre/modif/<int:id>', views.modifier_genre, name='modifier_genre'),
    path('genre_bands/<int:id>/', views.list_genre_bands, name='list_genre_bands'),
    path('band', views.list_bands, name='list_bands'),
    path('band/<int:id>/<str:redirect_to>', views.detail_band, name='detail_band'),
    path('band/ajout', views.ajout_band, name='ajout_band'),
    path('band/supp/<int:id>', views.supprimer_band, name='supprimer_band'),
    path('band/modif/<int:id>', views.modifier_band, name='modifier_band'),
    path('band/aimer/<int:id>', views.aimer_band, name='aimer_band'),
    path('band/a_ecouter/<int:id>', views.a_ecouter_band, name='a_ecouter_band'),
    path('band/inscrire_ecoute/<int:id>/<str:redirect_to>', views.inscrire_ecoute_band, name='inscrire_ecoute_band'),
    path('band/ne_pas_aimer/<int:id>', views.ne_pas_aimer_band, name='ne_pas_aimer_band'),
    path('bandlink/ajout/<int:band_id>/', views.ajout_bandlink, name='ajout_bandlink'),
    path('bandlink/supp/<int:band_id>/<int:id>', views.supprimer_bandlink, name='supprimer_bandlink'),
    path('band/choisir_pays/<int:id>', views.band_choisir_pays, name='band_choisir_pays'),
    path('band/ajout_pays/<int:band_id>/<int:id>', views.band_ajouter_pays, name='band_ajouter_pays'),
    path('band/enlever_pays/<int:band_id>/<int:id>', views.band_enlever_pays, name='band_enlever_pays'),
    path('band/choisir_genre/<int:id>', views.band_choisir_genre, name='band_choisir_genre'),
    path('band/ajout_genre/<int:band_id>/<int:id>', views.band_ajouter_genre, name='band_ajouter_genre'),
    path('band/enlever_genre/<int:band_id>/<int:id>', views.band_enlever_genre, name='band_enlever_genre'),
    path('band/liste_a_ecouter', views.liste_a_ecouter, name='liste_a_ecouter'),
    path('band/liste_ecoutes', views.liste_ecoutes, name='liste_ecoutes'),
    path('band/mes_bands', views.list_my_bands, name='list_my_bands'),
]
