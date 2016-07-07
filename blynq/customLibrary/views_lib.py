# import django.utils.timezone.datetime as datetime
import datetime
import logging

from django.core.mail import send_mail
from django.http import JsonResponse, Http404
from django.utils import timezone
import json, pytz
from authentication.models import UserDetails


def ajax_response(success=False, errors=[], obj_dict=None):
    context_dic = {'success': success, 'errors': errors}
    if obj_dict:
        for key in obj_dict.keys():
            context_dic[key] = obj_dict[key]
    return JsonResponse(context_dic, safe=False)


def get_userdetails(request):
    try:
        user_details = UserDetails.objects.get(user__username=request.user.username)
    except UserDetails.DoesNotExist:
        raise Http404("No UserDetails matches the given query. If you're logged in as django superuser please logout"
                      " and re-login as normal user")
    # user_details = default_userdetails()
    # organization = default_organization()
    return user_details


def string_to_dict(str):
    # json_acceptable_string = str.replace("'", "\"")
    try:
        obj = json.loads(str)
    except Exception as e:
        obj = {}
        debugFileLog.exception(e)
    return obj


def obj_to_json_str(obj):
    try:
        json_str = json.dumps(obj)
    except Exception as e:
        debugFileLog.exception(e)
        json_str = ''
    return json_str


def obj_to_json_response(obj):
    return JsonResponse(obj, safe=False)


def list_to_comma_string(list):
    return ','.join(map(str, list))


def send_mail_blynq(to=['hello@blynq.in'], subject='', message=''):
    try:
        send_mail(subject=subject, message=message, from_email='django@blynq.in', recipient_list=to,
                  fail_silently=False)
    except Exception as e:
        debugFileLog.error('Error while sending mail to ' + ','.join(to))


def default_string_to_datetime(str):
    """
    :param str: Format of the string is "%2d%2m%4Y%2H%2M%2S", example 31012016095455
    :return: dt: python datetime object in the utc timezone
    """
    dt = datetime.datetime.strptime(str, '%d%m%Y%H%M%S')
    dt = timezone.make_aware(dt, timezone.get_default_timezone())
    return dt


ist_timezone = pytz.timezone('Asia/Kolkata')
time_fmt = "%H:%M"
date_fmt = "%Y/%m/%d"
datetime_fmt = "%Y/%m/%d %H:%M"


def get_ist_datetime(utc_datetime):
    """
    :param utc_datetime: python datetime object in utc format
    :return: local_datetime : python datetime object in ist timezone
    """
    local_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(ist_timezone)
    return local_datetime


def generate_utc_datetime(ist_date, ist_time):
    """
    :param ist_date: python date object in the format "%Y/%m/%d"
    :param ist_time: python time object in the format "%H:%M"
    :return: utc_dt : python datetime object in utc timezone
    """
    ist_datetime = ist_date + ' ' + ist_time
    naive = datetime.datetime.strptime(ist_datetime, datetime_fmt)
    local_dt = ist_timezone.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt


def get_utc_datetime(ist_datetime):
    """
    :param ist_datetime: python datetime object in IST timezone
    :return: utc_datetime : python datetime object in UTC timezone
    """
    ist_date = ist_datetime.strftime(date_fmt)
    ist_time = ist_datetime.strftime(time_fmt)
    return generate_utc_datetime(ist_date=ist_date, ist_time=ist_time)


def get_ist_date_str(utc_datetime):
    """
    :param utc_datetime:
    :return:
    """
    ist_datetime = get_ist_datetime(utc_datetime=utc_datetime)
    ist_date = ist_datetime.strftime(date_fmt)
    return ist_date


def get_ist_time_str(utc_datetime):
    ist_datetime = get_ist_datetime(utc_datetime=utc_datetime)
    ist_time = ist_datetime.strftime(time_fmt)
    return ist_time


debugFileLog = logging.getLogger('debugFileLog')
consoleLog = logging.getLogger('consoleLog')
