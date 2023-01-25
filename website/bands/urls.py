from django.urls import path
from bands import views
#from accounts import views as accounts_views

app_name = 'bands'
urlpatterns = [
    # post views
    path('', views.home),
    path('country', bands.list_countries, name='list_countries'),
    path('country/<int:id>/', views.detail_country, name='detail_country'),
]
