from django.db import models
from django.utils import timezone

# Create your models here.
class Country(models.Model):
    country_alpha2 = models.CharField(max_length=2, null=False, unique=True)
    country_alpha3 = models.CharField(max_length=3, null=False, unique=True)
    country_name_fr = models.CharField(max_length=45, null=False, unique=True)
    country_name_en = models.CharField(max_length=45, null=False, unique=True)
    aud_crt_ts = models.DateTimeField(auto_now_add=True)
    aud_upd_ts = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['country_alpha2']

    def __sr__(self):
        return self.country_alpha2



