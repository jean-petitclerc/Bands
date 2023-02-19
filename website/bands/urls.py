from django.urls import path
from . import views
#from accounts import views as accounts_views

app_name = 'bands'
urlpatterns = [
    # post views
    path('', views.list_bands, name='list_bands'),
    path('country', views.list_countries, name='list_countries'),
    path('country/<int:id>/', views.detail_country, name='detail_country'),
    path('genre', views.list_genres, name='list_genres'),
    path('genre/<int:id>/', views.detail_genre, name='detail_genre'),
    path('genre/ajout', views.ajout_genre, name='ajout_genre'),
    path('genre/supp/<int:id>', views.supprimer_genre, name='supprimer_genre'),
    path('genre/modif/<int:id>', views.modifier_genre, name='modifier_genre'),
    path('band', views.list_bands, name='list_bands'),
    path('band/<int:id>/', views.detail_band, name='detail_band'),
    path('band/ajout', views.ajout_band, name='ajout_band'),
    path('band/supp/<int:id>', views.supprimer_band, name='supprimer_band'),
    path('band/modif/<int:id>', views.modifier_band, name='modifier_band'),
]
