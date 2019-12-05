
from django.http import JsonResponse
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point, Polygon
from ..models import Bakerie, Vote
from .serializers import serialize_bakeries
import json
from django.conf import settings
from typing import Tuple


def _get_long_lat(longlat: str) -> Tuple[float]:
    """
    Convert string to long lat
    """
    longlat = longlat[1:-1].split(",")
    longitude, latitude = float(longlat[0]), float(longlat[1])
    return longitude, latitude

def user_bakeries(request) -> JsonResponse:
    """
    Get bakeries related to user.
    """
    if request.user.is_authenticated:
        user_name = request.user.username
        user_votes_qset = Vote.objects.filter(
            user__username=user_name)  # .filter(bakerie__in=closest_bakery_qset)
        user_bakeries_qset = Bakerie.objects.filter(
            id__in=user_votes_qset.values_list("id"))

        gjson = serialize_bakeries(user_bakeries_qset, user_votes_qset)

        return JsonResponse(gjson)
    else:
        raise ConnectionRefusedError(
            "If user is not registrated, no bakeries to get")


def bakeries_arround(request, id_not_to_get: str,
                     longlat: str,
                     bbox_north_east: str,
                     bbox_south_west: str) -> JsonResponse:
    """
    Get closest bakeries from a point.
    id_not_to_get: pk of bakeries not to get
    bbox: borders of bouding box

    """

    id_not_to_get = id_not_to_get.split("-")

    longitude, latitude = _get_long_lat(longlat)

    ne = _get_long_lat(bbox_north_east)
    sw = _get_long_lat(bbox_south_west)
    xmin = sw[1]
    ymin = sw[0]
    xmax = ne[1]
    ymax = ne[0]
    bbox = ((ymax, xmin), (ymax, xmax),
            (ymin, xmax), (ymin, xmin), (ymax, xmin))

    user_name = request.user.username

    # Center point where to get arround bakeries
    center_point = Point(longitude, latitude, srid=4326)

    # Bounding box bakeries, to get only bakeries on a delimited area
    # Its also improve performances because we dont need to get all
    # the presents id of the map
    bbox = Polygon(bbox)

    if hasattr(settings, "FLANTASTIC_CLOSEST_ITEMS_NB"):
        CLOSEST_NB_ITEMS = settings.FLANTASTIC_CLOSEST_ITEMS_NB
    else:
        CLOSEST_NB_ITEMS = 20

    # Get closest bakeries limit 20 and in bbox
    bakeries_qset = Bakerie.objects.annotate(
        distance=Distance(
            'geom', center_point)
    ).filter(geom__intersects=bbox
             ).exclude(id__in=id_not_to_get
                       ).order_by('distance'
                                  )[0:CLOSEST_NB_ITEMS]

    # Get all votes related to users
    user_votes_qset = Vote.objects.filter(
        user__username=user_name).filter(bakerie__in=bakeries_qset)

    gjson = serialize_bakeries(bakeries_qset, user_votes_qset)
    return JsonResponse(gjson)