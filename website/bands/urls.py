from django.urls import path
from . import views
#from accounts import views as accounts_views

app_name = 'bands'
urlpatterns = [
    # post views
    path('', views.home, name='home'),
    path('country', views.list_countries, name='list_countries'),
    path('country/<int:id>/', views.detail_country, name='detail_country'),
    path('genre', views.list_genres, name='list_genres'),
    path('genre/<int:id>/', views.detail_genre, name='detail_genre'),
    path('genre/ajout', views.ajout_genre, name='ajout_genre'),
    path('genre/supp/<int:id>', views.supprimer_genre, name='supprimer_genre'),
    path('genre/modif/<int:id>', views.modifier_genre, name='modifier_genre'),
]
