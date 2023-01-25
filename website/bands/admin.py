from django.contrib import admin

# Register your models here.
from .models import Country
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['country_alpha2', 'country_alpha3', 'country_name_fr', 'country_name_en', 'aud_crt_ts', 'aud_upd_ts']
    search_fields = ['country_name_fr', 'country_name_en']
    ordering = ['country_name_fr']
