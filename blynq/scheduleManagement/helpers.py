from django.utils import timezone
from schedule.models import Rule
from customLibrary.views_lib import debugFileLog, list_to_comma_string, mail_exception, generate_utc_datetime, \
    get_ist_datetime, get_utc_datetime


BYWEEKDAY_DICT = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}
REVERSE_BYWEEKDAY_DICT = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}


def interval_param(interval):
    debugFileLog.info('inside interval_param')
    return 'interval:' + str(interval)


def list_to_param(key_str, bylistday):
    if bylistday:
        try:
            weekday_string = list_to_comma_string(bylistday)
            return key_str + ':' + weekday_string
        except Exception as e:
            mail_exception(exception=e)
    return ''


def append_params(params, new_keyvalue):
    if new_keyvalue:
        return params + ';' + new_keyvalue
    else:
        return params


def weekday_string_to_index(byweekday, reverse=False):
    new_byweekday = []
    if not byweekday:
        return new_byweekday
    mapping_dict = REVERSE_BYWEEKDAY_DICT if reverse else BYWEEKDAY_DICT
    for ele in byweekday:
        new_byweekday.append(mapping_dict[ele])
    return new_byweekday


# byweekday should be a list [0,2,3] meaning 0-Monday, 1-Tuesday, 2-Wednesday, 3-Thursday, 4-Friday, 5-Saturday,6-Sunday
def generate_rule_params(interval=1, bymonthday=None, byweekday=None, byweekno=None):
    debugFileLog.info("inside generate_rule_params")
    params = interval_param(interval)
    byweekday = weekday_string_to_index(byweekday)
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='byweekday', bylistday=byweekday))
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='bymonthday', bylistday=bymonthday))
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='byweekno', bylistday=byweekno))
    return params


def generate_rule(timeline, name, description):
    debugFileLog.info("inside generate_rule")
    interval = int(timeline.get('interval'))
    byweekno = timeline.get('byweekno')
    bymonthday = timeline.get('bymonthday')
    byweekday = timeline.get('byweekday')
    frequency = timeline.get('frequency')
    if not frequency:
        frequency = 'DAILY'
    params = generate_rule_params(interval=interval, bymonthday=bymonthday, byweekday=byweekday, byweekno=byweekno)
    rule = Rule(name=name, description=description, frequency=frequency, params=params)
    rule.save()
    return rule


def event_for_allday(schedule, timeline):
    debugFileLog.info("inside event_for_allday")
    start_date = timeline.get('start_date')
    start_time = "00:00:00"  # datetime.time(0)
    start = generate_utc_datetime(ist_date=start_date, ist_time=start_time)
    end_date = timeline.get('end_date')
    end_time = "23:59:59"  # datetime.time(23, 59, 59, 999)
    end = generate_utc_datetime(ist_date=end_date, ist_time=end_time)
    end_recurring_period_date = timeline.get('end_recurring_period')
    end_recurring_period = generate_utc_datetime(ist_date=end_recurring_period_date, ist_time=end_time)
    rule = generate_rule(timeline=timeline, name=schedule.schedule_title, description=schedule.schedule_title)
    creator = schedule.created_by.user if schedule.created_by else None
    event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': creator,
                  'rule': rule, 'end_recurring_period': end_recurring_period}
    return event_dict


def event_for_always(schedule):
    debugFileLog.info("inside event_for_always")
    ist_now = get_ist_datetime(timezone.now())
    ist_start = ist_now.replace(hour=0, minute=0, second=0)
    ist_end = ist_now.replace(hour=23, minute=59, second=59)
    start = get_utc_datetime(ist_start)
    end = get_utc_datetime(ist_end)
    rule = Rule(name=schedule.schedule_title, description=schedule.schedule_title, frequency='DAILY')
    rule.save()
    creator = schedule.created_by.user if schedule.created_by else None
    event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': creator,
                  'rule': rule, 'end_recurring_period': None}
    return event_dict


def event_dict_from_timeline(timeline, schedule):
    debugFileLog.info("insisde event_dict_from_timeline")
    is_always = timeline.get('is_always')
    all_day = timeline.get('all_day')
    is_repeat = timeline.get('is_repeat')
    recurrence_absolute = timeline.get('recurrence_absolute')
    if is_always is not None:
        schedule.is_always = is_always
    if all_day is not None:
        schedule.all_day = all_day
    if is_repeat is not None:
        schedule.is_repeat = is_repeat
    if recurrence_absolute is not None:
        schedule.recurrence_absolute = recurrence_absolute
    # TODO: validate whether commenting the below line is safe
    # schedule.save()
    if is_always:
        return event_for_always(schedule), schedule
    elif all_day:
        return event_for_allday(schedule, timeline), schedule
    else:
        start_date = timeline.get('start_date')
        start_time = timeline.get('start_time')
        start_time = start_time + ':00' if start_time else start_time
        start = generate_utc_datetime(ist_date=start_date, ist_time=start_time)
        end_date = timeline.get('end_date')
        end_time = timeline.get('end_time')
        end_time = end_time + ':59' if end_time else end_time
        end = generate_utc_datetime(ist_date=end_date, ist_time=end_time)
        end_recurring_period_time = end_time
        end_recurring_period = timeline.get('end_recurring_period')
        end_recurring_period = generate_utc_datetime(ist_date=end_recurring_period, ist_time=end_recurring_period_time)
        rule = generate_rule(timeline, name=schedule.schedule_title, description=schedule.schedule_title)
        creator = schedule.created_by.user if schedule.created_by else None
        event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': creator,
                      'rule': rule, 'end_recurring_period': end_recurring_period}
        return event_dict, schedule