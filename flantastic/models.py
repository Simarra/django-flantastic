# models.py
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.core.validators import MaxValueValidator, MinValueValidator
from statistics import mean
from django.contrib.auth import get_user_model

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


    geom = gismodels.PointField(srid=4326)

    @property
    def popupContent(self):
        res = self.enseigne + '\n' + self.commentaire
        if self.note is not None:
            res += self.note
        return res

    @property
    def globalnote(self):

        votes_for_bakerie = Vote.objects.filter(
            bakerie=self).values_list(flat=True)

        votes_for_bakerie = [i for i in votes_for_bakerie if i is not None]
        if len(votes_for_bakerie) >= 1:
            res = round(mean(votes_for_bakerie))
        else:
            res = None
        return res

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
    commentaire = models.CharField(max_length=256, blank=True)
    bakerie = models.ForeignKey(
        Bakerie,
        on_delete=models.CASCADE
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "id: " + str(self.id) + ", user: " + \
            str(self.user) + ", gout: " + str(self.gout) \
            + ", boulangerie: " + str(self.bakerie)
