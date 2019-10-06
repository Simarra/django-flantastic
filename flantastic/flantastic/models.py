# models.py
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.core.validators import MaxValueValidator, MinValueValidator


class Bakeries(gismodels.Model):

    FIVE_STARS_VALIDATOR = [MinValueValidator(1), MaxValueValidator(5)]

    id = models.AutoField(primary_key=True)
    enseigne = models.CharField(max_length=256)
    codpos = models.CharField(max_length=8)
    vmaj = models.CharField(max_length=256, null=True, default=None)
    vmaj1 = models.CharField(max_length=256, null=True, default=None)
    vmaj2 = models.CharField(max_length=256, null=True, default=None)
    vmaj3 = models.CharField(max_length=256, null=True, default=None)
    datemaj = models.CharField(max_length=256, null=True, default=None)

    pate = models.PositiveSmallIntegerField(
        validators=FIVE_STARS_VALIDATOR, null=True, default=None)
    texture = models.PositiveSmallIntegerField(
        validators=FIVE_STARS_VALIDATOR, null=True, default=None)
    gout = models.PositiveSmallIntegerField(
        validators=FIVE_STARS_VALIDATOR, null=True, default=None)
    apparence = models.PositiveSmallIntegerField(
        validators=FIVE_STARS_VALIDATOR)
    commentaire = models.CharField(max_length=256, null=True, default=None)

    geom = gismodels.PointField()

    def __unicode__(self):
        return self.enseigne
