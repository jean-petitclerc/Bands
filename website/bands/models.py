from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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


class Genre(models.Model):
    genre_name = models.CharField(max_length=50, null=False, unique=True)
    genre_desc = models.CharField(max_length=2048, null=True, blank=True, default='')
    aud_crt_user = models.ForeignKey(User,on_delete=models.RESTRICT, related_name='created_by')
    aud_crt_ts = models.DateTimeField(auto_now_add=True)
    aud_upd_user = models.ForeignKey(User,on_delete=models.RESTRICT, null=True, related_name='updated_by')
    aud_upd_ts = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['genre_name']

    def __str__(self):
        return self.genre_name

