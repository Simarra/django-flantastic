from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from djgeojson.serializers import Serializer as GeoJSONSerializer

from .models import Bakeries


def zoom_on_position(request):
    context = {}
    return render(request, 'maplayer.html', context)


def BoundariesGeoJSON(request):
    q_set = Bakeries.objects.all()[0:100]
    context = {'q_set': q_set}
    return render(request, 'maplayer.html', context)
