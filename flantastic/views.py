from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from djgeojson.serializers import Serializer as GeoJSONSerializer
from django.core.serializers import serialize
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from .models import Bakeries


def zoom_on_position(request):
    context = {}
    return render(request, 'maplayer.html', context)


def bakeries_arround(request):  # , longitude, latitude):
    """Get bakeries arround users and also ones filled
    """
    lattitude = 45.76894690751726
    longitude = 4.83203358225112

    user_pos = Point(longitude, lattitude, srid=4326)

    q_set = Bakeries.objects.annotate(distance=Distance(
        'geom', user_pos)).order_by('distance')[0:20]

    gjson = serialize('geojson', q_set, geometry_field="geom")
    return HttpResponse(gjson)
