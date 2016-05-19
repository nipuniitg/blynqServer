# import django.utils.timezone.datetime as datetime
import datetime
from django.http import JsonResponse, Http404
from django.utils import timezone
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


# Format of the string is 31012016095455
def default_string_to_datetime(str):
    dt=datetime.datetime.strptime(str,'%d%m%Y%H%M%S')
    dt = timezone.make_aware(dt, timezone.get_default_timezone())
    return dt


ist_timezone = pytz.timezone('Asia/Kolkata')
time_fmt = "%H:%M"
date_fmt = "%Y/%m/%d"
datetime_fmt = "%Y/%m/%d %H:%M"


# Delete the below function if not used
def get_ist_datetime(utc_datetime):
    local_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(ist_timezone)
    return local_datetime


def get_utc_datetime(ist_date, ist_time):
    ist_datetime = ist_date + ' ' + ist_time
    local = pytz.timezone ("Asia/Kolkata")
    naive = datetime.datetime.strptime (ist_datetime, datetime_fmt)
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)
    return utc_dt


def get_ist_date_str(utc_datetime):
    ist_datetime = get_ist_datetime(utc_datetime=utc_datetime)
    ist_date = ist_datetime.strftime(date_fmt)
    return ist_date


def get_ist_time_str(utc_datetime):
    ist_datetime = get_ist_datetime(utc_datetime=utc_datetime)
    ist_time = ist_datetime.strftime(time_fmt)
    return ist_time
