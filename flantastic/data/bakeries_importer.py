import csv
from django.contrib.gis.geos import Point

from flantastic.models import Bakeries
from .definitions import TMP_CSV, DELIMITER


def import_bakeries():
    reader = csv.DictReader(open(TMP_CSV, 'rt'), delimiter=DELIMITER)
    for line in reader:
        enseigne = str(line.pop("enseigne"))
        codpos = str(line.pop("codpos"))
        vmaj = str(line.pop("vmaj"))
        vmaj1 = str(line.pop("vmaj1"))
        vmaj2 = str(line.pop("vmaj2"))
        vmaj3 = str(line.pop("vmaj3"))
        datemaj = str(line.pop("datemaj"))
        lat = float(line.pop("latitude"))
        lng = float(line.pop("longitude"))

        res = Bakeries(enseigne=enseigne, geom=Point(
            lng, lat), datemaj=datemaj).save()
