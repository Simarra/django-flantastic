from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
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


def edit_bakerie(request):
    posts = get_object_or_404(Bakeries)
    response_data = {}

    if request.POST.get('action') == 'post':
        enseigne = request.POST.get('enseigne')
        commentaire = request.POST.get('commentaire')

        response_data['title'] = enseigne
        response_data['description'] = commentaire

        Bakeries.objects.create(
            enseigne=enseigne,
            commentaire=commentaire,
        )
        return JsonResponse(response_data)

    return render(request, 'create_post.html', {'posts': posts})


""" def edit_bakeries(request, pk):
    post = get_object_or_404(Bakeries, pk=pk)
    if request.method == "POST":
        form = BakeriesForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return JsonResponse(reponse_data)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form}) """
