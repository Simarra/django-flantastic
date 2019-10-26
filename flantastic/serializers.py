import json
from django.db.models import QuerySet
from django.core.serializers import serialize


def _update_dict_unsing_qset(dict_json: dict, q_set: QuerySet) -> dict:
    for feature in dict_json['features']:
        for vote in q_set:
            # Cache should be used
            if int(feature["properties"]["pk"]) == int(vote.bakerie.id):
                feature["properties"]["gout"] = vote.rate
            else:
                feature["properties"]["gout"] = None

    return dict_json


def serialize_bakeries(bakeries_qset: QuerySet, vote_qset: QuerySet):
    str_gjson = serialize('geojson', bakeries_qset, geometry_field="geom")
    dict_gjson = json.loads(str_gjson)

    res = _update_dict_unsing_qset(dict_gjson, vote_qset)

    res = json.dumps(res)

    return res

    
