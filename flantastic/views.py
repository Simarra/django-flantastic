from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


def zoom_on_position(request):
    context = {}
    return render(request, 'maplayer.html', context)