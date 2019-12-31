from django.test import TestCase
from flantastic.models import Bakerie, Vote
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from ..api.viewsets import _generate_bakery_qset
from ..views import edit_bakerie
from ..definitions import BAKERIE_API_SEND_FIELDS


class BakeriesAroundTestCase(TestCase):
    """
    High level test
    """

    def setUp(self):
        self.bak1 = Bakerie.objects.create(
            enseigne="BOULANGERIE BONNE", geom=Point(1, 2, srid=4326)
        )
        self.bak2 = Bakerie.objects.create(
            enseigne="BOULANGERIE BOF", geom=Point(1, 2, srid=4326)
        )
        self.user = User.objects.create_user(
            "john", "lennon@thebeatles.com", "johnpassword"
        )
        self.vote1 = Vote.objects.create(
            gout=1, pate=2, texture=3, apparence=4, bakerie=self.bak1, user=self.user
        )
        self.vote2 = Vote.objects.create(
            gout=1, pate=2, texture=3, apparence=4, bakerie=self.bak2, user=self.user
        )

    def test_around(self):
        """ Check basic function works. TODO: Test on working workstation."""
        center_point = Point(1, 2, srid=4326)
        bbox = Polygon.from_bbox((0, 0, 5, 5))
        id_not_to_get = 9999
        fields_to_get = BAKERIE_API_SEND_FIELDS
        closest_nb_items = 20

        res = _generate_bakery_qset(
            center_point, bbox, id_not_to_get, fields_to_get, closest_nb_items
        ).values_list()

        return True # TMP

    def test_only_wanted_colums_returned(self):
        return True
    

class BakerieSave(TestCase):
    """
    High level class
    Test that a bakery is well saved.
    """
    def SetUp(self):
        pass