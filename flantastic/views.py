from django.http import HttpResponse, Http404, JsonResponse, HttpRequest
from django.shortcuts import render
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from .models import Bakerie, Vote
from .serializers import serialize_bakeries
import json
from django.conf import settings


def zoom_on_position(request):
    context = {}
    return render(request, 'flantastic/maplayer.html', context)


def _get_bakeries_gjson_per_user(user_name: str, user_pos: Point) -> dict:
    """
    Gen a geojson containing bakeries and votes related.
    """

    CLOSEST_NB_ITEMS = settings.FLANTASTIC_CLOSEST_ITEMS_NB

    # Get all votes populated per user
    user_votes_qset = Vote.objects.filter(
        user__username=user_name)  # .filter(bakerie__in=closest_bakery_qset)

    # Get all bakeries populated per user
    user_bakeries_qset = Bakerie.objects.filter(id__in=user_votes_qset.values_list("id"))

    # Get closest bakeries limit 20
    closest_bakery_qset = Bakerie.objects.annotate(distance=Distance(
        'geom', user_pos)).order_by('distance')[0:CLOSEST_NB_ITEMS]

    # Get closests votes
    closest_votes_qset = Vote.objects.filter(bakerie__in=closest_bakery_qset)

    # get vote qset
    votes_qset = closest_votes_qset | user_votes_qset

    # get Bakerie Qset
    bakeries_qset = closest_bakery_qset | user_bakeries_qset
    print(bakeries_qset.query)
    print(votes_qset.query)

    gjson = serialize_bakeries(bakeries_qset, votes_qset)
    return gjson


# , longitude, latitude):
def bakeries_arround(request, longitude: str, latitude: str) -> JsonResponse:
    """Get bakeries arround users and also ones filled
    """
    try:
        latitude, longitude = float(latitude), float(longitude)
    except ValueError:
        raise Http404("invalide lat long type")

    user_pos = Point(longitude, latitude, srid=4326)

    gjson = _get_bakeries_gjson_per_user(str(request.user), user_pos)
    return JsonResponse(gjson)


def edit_bakerie(request: HttpRequest):
    """
    Edition of existing bakerie.
    If no vote is exising, it is created.
    """
    if request.method == 'POST':
        if request.user.is_authenticated:
            data: dict = json.loads(request.body)

            # Update bakerie
            bakery = Bakerie.objects.filter(pk=data["pk"]).first()
            bakery.enseigne = data["enseigne"]
            bakery.save()

            # Update vote
            vote_q_set = Vote.objects.filter(
                bakerie__id=data["pk"]).filter(
                    user=request.user
            )

            if vote_q_set.exists():
                vote = vote_q_set.first()
                vote.commentaire = data["commentaire"]
                vote.gout = data["gout"]
                vote.pate = data["pate"]
                vote.texture = data["texture"]
                vote.apparence = data["apparence"]
            else:
                vote = Vote(
                    commentaire=data["commentaire"],
                    gout=data["gout"],
                    pate=data["pate"],
                    texture=data["texture"],
                    apparence=data["apparence"],
                    user=request.user,
                    bakerie=bakery.get()
                )
            vote.save()
            bakery.refresh_from_db()
            data["global_note"] = bakery.global_note

            return JsonResponse(data)
        else:
            raise ConnectionRefusedError("Impossible to post if not logged")
