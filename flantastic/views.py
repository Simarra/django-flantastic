from django.http import HttpResponse, Http404, JsonResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from .models import Bakerie, Vote
from .serializers import serialize_bakeries
import json
from django.contrib.auth import get_user_model


def zoom_on_position(request):
    context = {}
    return render(request, 'flantastic/maplayer.html', context)


def _get_bakeries_gjson_per_user(user_name: str, user_pos: Point):

    bakeries_set = Bakerie.objects.annotate(distance=Distance(
        'geom', user_pos)).order_by('distance')[0:20]

    rates_set = Vote.objects.filter(
        user__username=user_name).filter(bakerie__in=bakeries_set)

    gjson = serialize_bakeries(bakeries_set, rates_set)
    return gjson


# , longitude, latitude):
def bakeries_arround(request, longitude: str, latitude: str):
    """Get bakeries arround users and also ones filled
    """
    try:
        latitude, longitude = float(latitude), float(longitude)
    except ValueError:
        raise Http404("invalide lat long type")

    user_pos = Point(longitude, latitude, srid=4326)

    gjson = _get_bakeries_gjson_per_user(str(request.user), user_pos)
    return HttpResponse(gjson)


def edit_bakerie(request: HttpRequest):
    """
    Edition of existing bakerie.
    If no vote is exising, it is created.
    """
    if request.method == 'POST':
        if request.user.is_authenticated:
            data: dict = json.loads(request.body)

            # Update bakerie
            Bakerie.objects.filter(pk=data["pk"]).update(
                enseigne=data["enseigne"],
            )

            # Update vote
            vote = Vote.objects.filter(
                bakerie__id=data["pk"]).filter(
                    user=request.user
            )

            vote.update(
                commentaire=data["commentaire"],
                gout=data["gout"],
                pate=data["pate"],
                texture=data["texture"],
                apparence=data["apparence"]
            )

            return JsonResponse(data)
        else:
            raise ConnectionRefusedError("Impossible to post if not logged")
    # print("COUCOU")

    # posts = get_object_or_404(Bakerie)
    # return render(request, 'create_post.html', {'posts': posts})


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
