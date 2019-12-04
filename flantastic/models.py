# models.py
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.core.validators import MaxValueValidator, MinValueValidator
from statistics import mean
from django.contrib.auth import get_user_model
from django.db.models import Avg


User = get_user_model()


FIVE_STARS_VALIDATOR = [MinValueValidator(1), MaxValueValidator(5)]


class Bakerie(gismodels.Model):

    id = models.AutoField(primary_key=True)
    enseigne = models.CharField(max_length=256)
    codpos = models.CharField(max_length=8, blank=True)
    commune = models.CharField(max_length=256, blank=True)
    siren = models.BigIntegerField(null=True)
    vmaj = models.CharField(max_length=256, null=True, default=None)
    vmaj1 = models.CharField(max_length=256, null=True, default=None)
    vmaj2 = models.CharField(max_length=256, null=True, default=None)
    vmaj3 = models.CharField(max_length=256, null=True, default=None)
    datemaj = models.CharField(max_length=256, null=True, default=None)

    modified_date = models.DateTimeField(auto_now=True, null=True)
    global_note = models.FloatField(
        validators=FIVE_STARS_VALIDATOR, null=True, default=None)

    geom = gismodels.PointField(srid=4326)

    def update_global_note(self) -> None:
        """
        Triggered when a vote is save to update global
        note of the establishment
        """

        votes_for_bakerie = Vote.objects.filter(
            bakerie=self)

        criterias_fields = ["gout", "texture", "pate", "apparence"]

        avgs = [Avg(i) for i in criterias_fields]
        aggr_dict = votes_for_bakerie.aggregate(*avgs)
        res = mean(aggr_dict.values())

        self.global_note = res
        self.save()

    def __str__(self):
        return self.enseigne


class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    gout = models.PositiveSmallIntegerField(
        validators=FIVE_STARS_VALIDATOR, null=True, default=None)
    pate = models.PositiveSmallIntegerField(
        validators=FIVE_STARS_VALIDATOR, null=True, default=None)
    texture = models.PositiveSmallIntegerField(
        validators=FIVE_STARS_VALIDATOR, null=True, default=None)
    apparence = models.PositiveSmallIntegerField(
        validators=FIVE_STARS_VALIDATOR, null=True, default=None)
    commentaire = models.CharField(max_length=500, blank=True)
    bakerie = models.ForeignKey(
        Bakerie,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    modified_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "id: " + str(self.id) + ", user: " + \
            str(self.user) + ", gout: " + str(self.gout) \
            + ", boulangerie: " + str(self.bakerie)
