# models.py
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.core.validators import MaxValueValidator, MinValueValidator


class Bakeries(gismodels.Model):

    FIVE_STARS_VALIDATOR = [MinValueValidator(1), MaxValueValidator(5)]

    id = models.IntegerField(primary_key=True)
    enseigne = models.CharField(max_length=256)
    codpos = models.CharField(max_length=8)
    vmaj = models.CharField(max_lenght=256)
    vmaj1 = models.CharField(max_lenght=256)
    vmaj2 = models.CharField(max_lenght=256)
    vmaj3 = models.CharField(max_lenght=256)
    datemaj = models.CharField(max_lenght=256)

    pate = models.PositiveSmallIntegerField(validators=FIVE_STARS_VALIDATOR)
    texture = models.PositiveSmallIntegerField(validators=FIVE_STARS_VALIDATOR)
    gout = models.PositiveSmallIntegerField(validators=FIVE_STARS_VALIDATOR)
    apparence = models.PositiveSmallIntegerField(
        validators=FIVE_STARS_VALIDATOR)
    commentaire = models.CharField(max_length=256)

    geom = gismodels.PointField()

    objects = gismodels.GeoManager()

    def __unicode__(self):
        return self.enseigne
