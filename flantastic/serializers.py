import json
from django.db.models import QuerySet
from django.core.serializers import serialize
from copy import deepcopy


def _update_dict_unsing_qset(dict_json: dict, q_set: QuerySet) -> dict:
    """
    Sub function wich make the join in python 
    betwenn queryset and dict.
    """

    def _update_dict_features(dict_js: dict, idx: int,
                              vote) -> dict:
        """
        Avoid to by DRY
        """
        f_names = ["pate", "texture", "apparence", "commentaire", "gout"]
        if vote is None:
            for elt in f_names:
                dict_js["features"][idx]["properties"][elt] = None
        else:
            for elt in f_names:
                dict_js["features"][idx]["properties"][elt] = getattr(
                    vote, elt)
        return dict_js

    # Copy the dict because never iterate on a dict being updated
    dict_json_copy = deepcopy(dict_json)

    for idx, val in enumerate(dict_json_copy['features']):
        if q_set.exists:
            for vote in q_set:
                # Cache should be used
                if int(val["properties"]["pk"]) == int(vote.bakerie.id):
                    dict_json = _update_dict_features(dict_json, idx, vote)
                    break
            else:
                dict_json = _update_dict_features(dict_json, idx, None)
        else:
            dict_json = _update_dict_features(dict_json, idx, None)

    del(dict_json_copy)
    return dict_json


def serialize_bakeries(bakeries_qset: QuerySet, vote_qset: QuerySet) -> dict:
    str_gjson = serialize('geojson', bakeries_qset, geometry_field="geom")
    dict_gjson = json.loads(str_gjson)

    res = _update_dict_unsing_qset(dict_gjson, vote_qset)


    return res
