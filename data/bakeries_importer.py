import csv
from django.contrib.gis.geos import Point

from flantastic.flantastic.models import Bakeries
from .definitions import TMP_CSV, DELIMITER


reader = csv.DictReader(open(TMP_CSV, 'rb'), delimiter=DELIMITER)
for line in reader:
    enseigne = str(line.pop("enseigne"))
    codpos = str(line.pop("codpos"))
    vmaj = str(line.pop("vmaj"))
    vmaj1 = str(line.pop("vmaj1"))
    vmaj2 = str(line.pop("vmaj2"))
    vmaj3 = str(line.pop("vmaj3"))
    datema = str(line.pop("datemaj"))
    lat = float(line.pop("latitude"))
    lng = float(line.pop("longitude"))




    Bakeries(enseigne=enseigne, geom=Point(lng, lat))
    import pdb; pdb.set_trace()
    # Bakeries.save()
