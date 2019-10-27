import json
from django.db.models import QuerySet
from django.core.serializers import serialize


def _update_dict_unsing_qset(dict_json: dict, q_set: QuerySet) -> dict:
    for feature in dict_json['features']:
        if len(q_set) > 0:
            for vote in q_set:
                # Cache should be used
                if int(feature["properties"]["pk"]) == int(vote.bakerie.id):
                    feature["properties"]["pate"] = vote.pate
                    feature["properties"]["texture"] = vote.texture
                    feature["properties"]["apparence"] = vote.apparence
                    feature["properties"]["commentaire"] = vote.commentaire
                    feature["properties"]["gout"] = vote.gout
                else:
                    feature["properties"]["pate"] = None
                    feature["properties"]["texture"] = None
                    feature["properties"]["apparence"] = None
                    feature["properties"]["commentaire"] = None
                    feature["properties"]["gout"] = None
        else:
            feature["properties"]["pate"] = None
            feature["properties"]["texture"] = None
            feature["properties"]["apparence"] = None
            feature["properties"]["commentaire"] = None
            feature["properties"]["gout"] = None
            print(feature)

    return dict_json


def serialize_bakeries(bakeries_qset: QuerySet, vote_qset: QuerySet):
    str_gjson = serialize('geojson', bakeries_qset, geometry_field="geom")
    dict_gjson = json.loads(str_gjson)

    res = _update_dict_unsing_qset(dict_gjson, vote_qset)

    res = json.dumps(res)

    return res

    
