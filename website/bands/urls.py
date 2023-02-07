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
]
