from django.http import HttpResponse, Http404, JsonResponse, HttpRequest
from django.shortcuts import render
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point, Polygon
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
    user_bakeries_qset = Bakerie.objects.filter(
        id__in=user_votes_qset.values_list("id"))

    # Get closest bakeries limit 20
    closest_bakery_qset = Bakerie.objects.annotate(distance=Distance(
        'geom', user_pos)).order_by('distance')[0:CLOSEST_NB_ITEMS]

    # Get closests votes
    closest_votes_qset = Vote.objects.filter(bakerie__in=closest_bakery_qset)

    # get vote qset
    votes_qset = closest_votes_qset | user_votes_qset

    # get Bakerie Qset
    bakeries_qset = closest_bakery_qset | user_bakeries_qset

    gjson = serialize_bakeries(bakeries_qset, votes_qset)
    return gjson


def bakeries_arround(request, longlat: str) -> JsonResponse:
    """
    Get bakeries arround a point 
    """
    longlat = longlat[1:-1].split(",")
    longitude, latitude = float(longlat[0]), float(longlat[1])

    user_name = request.user.username

    user_pos = Point(longitude, latitude, srid=4326)

    CLOSEST_NB_ITEMS = settings.FLANTASTIC_CLOSEST_ITEMS_NB

    # Get closest bakeries limit 20
    bakeries_qset = Bakerie.objects.annotate(distance=Distance(
        'geom', user_pos)).order_by('distance')[0:CLOSEST_NB_ITEMS]

    # Get all votes related to users
    user_votes_qset = Vote.objects.filter(
        user__username=user_name).filter(bakerie__in=bakeries_qset)

    gjson = serialize_bakeries(bakeries_qset, user_votes_qset)
    return JsonResponse(gjson)


def user_bakeries(request) -> JsonResponse:
    """
    Get bakeries related to user.
    """
    if request.user.is_authentificated:
        user_votes_qset = Vote.objects.filter(
            user__username=user_name)  # .filter(bakerie__in=closest_bakery_qset)
        user_bakeries_qset = Bakerie.objects.filter(
            id__in=user_votes_qset.values_list("id"))

        gjson = serialize_bakeries(user_bakeries_qset, user_votes_qset)

        return JsonResponse(gjson)
    else:
        raise ConnectionRefusedError(
            "If user is not registrated, no bakeries to get")


def bakeries_arround_2(request, longitude: str, latitude: str, id_not_to_get: str, bbox_top_left: str, bbox_top_right: str, bbox_bottom_left: str, bbox_bottom_right: str) -> JsonResponse:
    """
    Get closest bakeries from a point.
    id_not_to_get: pk of bakeries not to get
    bbox: borders of bouding box

    """
    try:
        latitude, longitude, bbox_top_left, bbox_top_right, bbox_bottom_left, bbox_bottom_right = float(latitude), float(
            longitude), float(bbox_top_left), float(bbox_top_right), float(bbox_bottom_left), float(bbox_bottom_right)
        id_not_to_get = id_not_to_get.split("-")
    except ValueError as e:
        raise Http404("invalid parameter transformation", e)

    user_name = request.user.username

    # Center point where to get arround bakeries
    center_point = Point(longitude, latitude, srid=4326)

    # Bounding box bakeries, to get only bakeries on a delimited area
    # Its also improve performances because we dont need to get all
    # the presents id of the map
    bbox = Polygon((bbox_top_left,
                    bbox_bottom_right,
                    bbox_bottom_left,
                    bbox_bottom_right))

    CLOSEST_NB_ITEMS = settings.FLANTASTIC_CLOSEST_ITEMS_NB

    # Get closest bakeries limit 20 and in bbox
    bakeries_qset = Bakerie.objects.annotate(
        distance=Distance(
            'geom', center_point)
            ).order_by('distance'
            ).filter(geom__intersects=bbox
            )[0:CLOSEST_NB_ITEMS]


    # Get all votes related to users
    user_votes_qset = Vote.objects.filter(
        user__username=user_name).filter(bakerie__in=bakeries_qset)

    gjson = serialize_bakeries(bakeries_qset, user_votes_qset)
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
