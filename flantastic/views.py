from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.serializers import serialize
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from .models import Bakeries


def zoom_on_position(request):
    context = {}
    return render(request, 'flantastic/maplayer.html', context)


def bakeries_arround(request, longitude, latitude):  # , longitude, latitude):
    """Get bakeries arround users and also ones filled
    """
    try:
        latitude, longitude = float(latitude), float(longitude)
    except ValueError:
        raise Http404("invalide lat long type")

    user_pos = Point(longitude, latitude, srid=4326)

    q_set = Bakeries.objects.annotate(distance=Distance(
        'geom', user_pos)).order_by('distance')[0:20]

    gjson = serialize('geojson', q_set, geometry_field="geom")
    return HttpResponse(gjson)
