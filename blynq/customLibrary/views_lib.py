# import django.utils.timezone.datetime as datetime
from time import time
import functools
import logging
import subprocess
import re
import json, pytz, os

import datetime
from django.core.mail import send_mail
from django.db import connection, reset_queries
from django.http import JsonResponse, Http404
from django.utils import timezone

from blynq.settings import MEDIA_ROOT, DEBUG


def send_mail_blynq(to=['hello@blynq.in'], subject='', message=''):
    if DEBUG:
        return
    try:
        send_mail(subject=subject, message=message, from_email='django@blynq.in', recipient_list=to,
                  fail_silently=False)
    except Exception as e:
        debugFileLog.error('Error while sending mail to ' + ','.join(to))


def mail_exception(exception, to=['nipun@blynq.in'], subject='Recieved exception'):
    exception = str(exception)
    debugFileLog.exception(exception)
    send_mail_blynq(to=to, subject=subject, message=exception)


def ajax_response(success=False, errors=[], obj_dict=None):
    context_dic = {'success': success, 'errors': errors}
    if obj_dict:
        for key in obj_dict.keys():
            context_dic[key] = obj_dict[key]
    return JsonResponse(context_dic, safe=False)


def get_userdetails(request):
    try:
        from authentication.models import UserDetails
        user_details = UserDetails.objects.get(user__username=request.user.username)
    except UserDetails.DoesNotExist:
        raise Http404("No UserDetails matches the given query. If you're logged in as django superuser please logout"
                      " and re-login as normal user")
    # user_details = default_userdetails()
    # organization = default_organization()
    return user_details


def string_to_dict(str):
    # apostrophe is not working if the below line is uncommented
    # json_acceptable_string = str.replace("'", "\"")
    try:
        obj = json.loads(str)
    except Exception as e:
        obj = {}
        debugFileLog.exception('Exception in string_to_dict for str: %s' % str)
        mail_exception(exception=e)
    return obj


def obj_to_json_str(obj):
    try:
        json_str = json.dumps(obj)
    except Exception as e:
        debugFileLog.exception(str(obj))
        mail_exception(exception=e)
        json_str = ''
    return json_str


def obj_to_json_response(obj):
    return JsonResponse(obj, safe=False)


def list_to_comma_string(list):
    return ','.join(map(str, list))


def empty_list_for_none(obj):
    if obj:
        return obj
    else:
        return []


def empty_string_for_none(obj):
    if obj:
        return obj
    else:
        return ''


def default_string_to_datetime(str, fmt='%d%m%Y%H%M%S'):
    """
    :param fmt: format of the date string can be mentioned
    :param str: Format of the string is "%2d%2m%4Y%2H%2M%2S", example 31012016095455
    :return: dt: python datetime object in the utc timezone
    """
    dt = datetime.datetime.strptime(str,fmt)
    dt = timezone.make_aware(dt, timezone.get_default_timezone())
    return dt


ist_timezone = pytz.timezone('Asia/Kolkata')
time_fmt = "%H:%M"
time_fmt_with_seconds = "%H:%M:%S"
date_fmt = "%Y/%m/%d"
datetime_fmt = "%Y/%m/%d %H:%M"
datetime_fmt_with_seconds = "%Y/%m/%d %H:%M:%S"


def get_video_length(file_path):
    default_video_duration = 120
    try:
        result = subprocess.Popen('ffprobe -i "%s" -show_entries format=duration -v quiet -of csv="p=0"' % file_path,
                                  stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        output = result.communicate()
        durations = re.findall("\d+", output[0])
        duration = int(durations[0]) if durations else default_video_duration
        return duration
    except Exception as e:
        debugFileLog.exception('Error received for file_path: %s' % file_path)
        mail_exception(exception=e)
        return default_video_duration


def get_ist_datetime(utc_datetime):
    """
    :param utc_datetime: python datetime object in utc format
    :return: local_datetime : python datetime object in ist timezone
    """
    local_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(ist_timezone)
    return local_datetime


def generate_utc_datetime(ist_date, ist_time, seconds_str=''):
    """
    :param seconds_str: Just a hack to enable schedules to play till 23:59:59 instead of 23:59
    :param ist_date: python date object in the format "%Y/%m/%d"
    :param ist_time: python time object in the format "%H:%M"
    :return: utc_dt : python datetime object in utc timezone
    """
    ist_datetime = ist_date + ' ' + ist_time
    if seconds_str:
        required_fmt = datetime_fmt_with_seconds
        ist_datetime = ist_datetime + ':' + seconds_str
    else:
        required_fmt = datetime_fmt
    naive = datetime.datetime.strptime(ist_datetime, required_fmt)
    local_dt = ist_timezone.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt


def get_utc_datetime(ist_datetime, include_seconds=False):
    """
    :param include_seconds: Player do need seconds but the portal doesn't need seconds
    :param ist_datetime: python datetime object in IST timezone
    :return: utc_datetime : python datetime object in UTC timezone
    """
    ist_date = ist_datetime.strftime(date_fmt)
    ist_time = ist_datetime.strftime(time_fmt)
    # TODO: Fix this bug
    # if include_seconds:
    #     ist_time = ist_datetime.strftime(time_fmt_with_seconds)
    # else:
    #     ist_time = ist_datetime.strftime(time_fmt)
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


def date_changed(received_datetime):
    if received_datetime.date() < timezone.now().date():
        return True
    else:
        return False


def datetime_to_string(datetime_obj, fmt=datetime_fmt):
    return datetime_obj.strftime(fmt)


def date_to_string(date_obj, fmt=date_fmt):
    return date_obj.strftime(fmt)


def string_to_date(date_str, fmt=date_fmt):
    return datetime.datetime.strptime(date_str, fmt).date()


def today_date():
    return timezone.now().date()


def full_file_path(relative_path=''):
    return os.path.join(MEDIA_ROOT, relative_path)


def timeit(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time()
        response = func(*args, **kwargs)
        elapsedTime = time() - startTime
        debugFileLog.info('function [{}] finished in {} ms'.format(func.__name__, int(elapsedTime * 1000)))
        return response
    return newfunc


# Decorator function to log query times during debugging
def log_query_times(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        if DEBUG:
            reset_queries()
        response = func(*args, **kwargs)
        if DEBUG:
            top_results = 10
            queries = connection.queries
            debugFileLog.info('Inside log_query_times, total queries %d' % len(queries))
            newlist = sorted(queries, key=lambda k: float(k['time']))
            top_results = len(queries) if len(queries) < 10 else 10
            newlist.reverse()
            for i in range(top_results):
                debugFileLog.info('Time ' + newlist[i]['time'] + ' Query: ' + newlist[i]['sql'])
        return response
    return newfunc


def wrap_try_catch(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except Exception as e:
            mail_exception(exception=e)

debugFileLog = logging.getLogger('debugFileLog')
consoleLog = logging.getLogger('consoleLog')