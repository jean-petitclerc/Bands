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
    aud_crt_user = models.ForeignKey(User,on_delete=models.RESTRICT, related_name='genre_created_by')
    aud_crt_ts = models.DateTimeField(auto_now_add=True)
    aud_upd_user = models.ForeignKey(User,on_delete=models.RESTRICT, null=True, related_name='genre_updated_by')
    aud_upd_ts = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['genre_name']

    def __str__(self):
        return self.genre_name


class Band(models.Model):
    band_name = models.CharField(max_length=50, null=False, unique=True)
    band_desc = models.CharField(max_length=2048, null=True, blank=True, default='')
    aud_crt_user = models.ForeignKey(User,on_delete=models.RESTRICT, related_name='band_created_by')
    aud_crt_ts = models.DateTimeField(auto_now_add=True)
    aud_upd_user = models.ForeignKey(User,on_delete=models.RESTRICT, null=True, related_name='band_updated_by')
    aud_upd_ts = models.DateTimeField(auto_now=True, null=True)
    plays_genres = models.ManyToManyField(Genre, related_name='genre_played_by_bands')
    from_countries = models.ManyToManyField(Country, related_name='created_bands')
    has_fans = models.ManyToManyField(User, related_name='is_fan_of')
    #comments = db.relationship('BandComment', backref='tband', lazy='dynamic')

    class Meta:
        ordering = ['band_name']

    def __str__(self):
        return self.band_name


class BandLink(models.Model):
    class LinkName(models.TextChoices):
        WIKIPEDIA = 'Wikipedia', 'Wikipedia'
        METALARCHIVE = 'Metal Archive', 'Metal Archive'
        YOUTUBEMUSIC = 'YouTube Music', 'YouTube Music'
    link_name = models.CharField(max_length=32, null=False, choices=LinkName.choices, default=LinkName.METALARCHIVE)
    link_url = models.URLField(null=False)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='link_for_a_band')
    aud_crt_user = models.ForeignKey(User,on_delete=models.RESTRICT, related_name='bandlink_created_by')
    aud_crt_ts = models.DateTimeField(auto_now_add=True)
    aud_upd_user = models.ForeignKey(User,on_delete=models.RESTRICT, null=True, related_name='bandlink_updated_by')
    aud_upd_ts = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.band.band_name + ':' + self.link_name


class BandAEcouter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_be_listened_by')
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='bands_to_listen')
    added_ts = models.DateTimeField(auto_now_add=True)
    listened_ts = models.DateTimeField(null=True, default=None)

    class Meta:
        ordering = ['added_ts']

