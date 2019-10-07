from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from djgeojson.serializers import Serializer as GeoJSONSerializer
from django.core.serializers import serialize

from .models import Bakeries


def zoom_on_position(request):
    context = {}
    return render(request, 'maplayer.html', context)


def bakeries_arround(request):#, longitude, latitude):
    """Get bakeries arround users and also ones filled
    """
    q_set = Bakeries.objects.all()[0:100]
    gjson = serialize('geojson', q_set, geometry_field="geom")
    return HttpResponse(gjson)
