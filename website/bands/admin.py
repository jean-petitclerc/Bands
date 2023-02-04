from django.contrib import admin

# Register your models here.
from .models import Country, Genre


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['country_alpha2', 'country_alpha3', 'country_name_fr', 'country_name_en', 'aud_crt_ts', 'aud_upd_ts']
    search_fields = ['country_name_fr', 'country_name_en']
    ordering = ['country_name_fr']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre_name', 'genre_desc', 'aud_crt_user_id', 'aud_crt_ts', 'aud_upd_user_id', 'aud_upd_ts']
    search_fields = ['genre_name']
    ordering = ['genre_name']
