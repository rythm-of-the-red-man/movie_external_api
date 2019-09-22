from django.db import models
from django.utils.translation import gettext as _
# Create your models here.


class Movie(models.Model):

    title = models.CharField(_('Title'),max_length=128)
    runtime = models.CharField(max_length=24, blank=True, null=True)
    genre = models.CharField(max_length=128, blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    type = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")

    def __str__(self):
        return self.title


class ImdbInfo(models.Model):

    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    imdbrating = models.FloatField( blank=True, null=True)
    imdbvotes = models.IntegerField( blank=True, null=True)
    imdbid = models.CharField(max_length=12, blank=True, null=True)
    metascore = models.IntegerField( blank=True, null=True)

    class Meta:
        verbose_name = _("ImdbInfo")
        verbose_name_plural = _("ImdbInfos")


class Staff(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    director = models.CharField(max_length=64, blank=True, null=True)
    writer = models.TextField(max_length=512, blank=True, null=True)
    actors = models.TextField(max_length=512, blank=True, null=True)

    class Meta:
        verbose_name = _("Staff")
        verbose_name_plural = _("Staff")


class Timeline(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    year = models.DateField( blank=True, null=True)
    released = models.DateField(blank=True, null=True)
    dvd = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = _("Timeline")
        verbose_name_plural = _("Timelines")


class MarketingInfo(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    boxoffice = models.IntegerField(blank=True, null=True)
    production = models.CharField(max_length=64, blank=True, null=True)
    website = models.URLField( blank=True, null=True)
    poster = models.URLField( blank=True, null=True)
    rated = models.CharField(max_length=32, blank=True, null=True)
    awards = models.TextField( blank=True, null=True)

    class Meta:
        verbose_name = _("MarketingInfo")
        verbose_name_plural = _("MarketingInfos")


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    source = models.CharField(max_length=64, blank=True, null=True)
    value = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")

class Comment(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    comment = models.TextField(max_length=255, blank=False)
    date_of_creation = models.DateField(auto_now=True)

