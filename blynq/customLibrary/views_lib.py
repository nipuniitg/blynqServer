from django.http import JsonResponse
import json

from authentication.models import UserDetails


def ajax_response(success=False, errors=[], obj_dict=None):
    context_dic = {}
    context_dic['success'] = success
    context_dic['errors'] = errors
    for key in obj_dict.keys():
        context_dic[key] = obj_dict[key]
    return JsonResponse(context_dic, safe=False)


def user_and_organization(request):
    user_details = UserDetails.objects.get(username=request.user.username)
    organization = user_details.organization
    # user_details = default_userdetails()
    # organization = default_organization()
    return user_details, organization


def string_to_dict(str):
    #json_acceptable_string = str.replace("'", "\"")
    return json.loads(str)


def list_to_json(list):
    return JsonResponse(list, safe=False)