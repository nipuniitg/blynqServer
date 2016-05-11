from django.http import JsonResponse, Http404
import json, pytz

from authentication.models import UserDetails

def ajax_response(success=False, errors=[], obj_dict=None):
    context_dic = {}
    context_dic['success'] = success
    context_dic['errors'] = errors
    if obj_dict:
        for key in obj_dict.keys():
            context_dic[key] = obj_dict[key]
    return JsonResponse(context_dic, safe=False)


def get_userdetails(request):
    try:
        user_details = UserDetails.objects.get(username=request.user.username)
    except UserDetails.DoesNotExist:
        raise Http404("No UserDetails matches the given query. If you're logged in as django superuser please logout"
                      " and re-login as normal user")
    # user_details = default_userdetails()
    # organization = default_organization()
    return user_details


def string_to_dict(str):
    # json_acceptable_string = str.replace("'", "\"")
    return json.loads(str)


def list_to_json(list):
    return JsonResponse(list, safe=False)


def list_to_comma_string(list):
    return ','.join(map(str, list))

local_timezone = pytz.timezone('Asia/Kolkata')


# Delete the below function if not used
def get_local_time(utc_datetime):
    local_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_datetime
