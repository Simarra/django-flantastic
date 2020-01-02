from django.test import TestCase
from flantastic.models import Bakerie, Vote
from django.contrib.gis.geos import Point, Polygon
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

        self.center_point = Point(1, 2, srid=4326)
        self.bbox = Polygon.from_bbox((0, 0, 5, 5))
        self.id_not_to_get = [
            "9999",
        ]
        self.fields_to_get = BAKERIE_API_SEND_FIELDS
        self.closest_nb_items = 20

    def test_around_len_objects(self):
        """ Check basic function works. TODO: Test on working workstation."""

        res = _generate_bakery_qset(
            self.center_point,
            self.bbox,
            self.id_not_to_get,
            self.fields_to_get,
            self.closest_nb_items,
        )
        res = len(res)
        self.assertEqual(res, 2)


    def test_only_wanted_colums_returned(self):
        res = _generate_bakery_qset(
            self.center_point,
            self.bbox,
            self.id_not_to_get,
            self.fields_to_get,
            self.closest_nb_items,
        ).values()
        list_result = [e for e in res]

        for row in list_result:
            self.assertin("enseigne", row.keys())

class BakerieSave(TestCase):
    """
    High level class
    Test that a bakery is well saved.
    """

    def SetUp(self):
        pass
