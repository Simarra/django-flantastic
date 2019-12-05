from django.test import TestCase
from flantastic.models import Bakerie, Vote
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User

class BakerieTestCase(TestCase):
    def setUp(self):
        self.bak1 = Bakerie.objects.create(enseigne="BOULANGERIE BONNE" , geom=Point(1,2, srid=4326))
        self.bak2 = Bakerie.objects.create(enseigne="BOULANGERIE BOF", geom=Point(1,2, srid=4326) )
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_vote_can_be_created(self):
        """Animals that can speak are correctly identified"""
        vote = Vote.objects.create(gout=1, pate=2, texture=3, apparence=4, bakerie=self.bak1, user=self.user)
        return True
    
    def test_bakery_single_user_note_update_triggered(self):
        """ Global note must be updated"""
        vote = Vote.objects.create(gout=1, pate=2, texture=3, apparence=4, bakerie=self.bak1, user=self.user)
        self.assertIsNone(self.bak1.global_note)
        self.assertIsNot(self.bak1.global_note, float(0))