from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.shortcuts import render
from schedule.models import Calendar

from authentication.models import City
from authentication.serializers import CitySerializer
from customLibrary.views_lib import ajax_response, get_userdetails, string_to_dict, obj_to_json_response, debugFileLog
from screenManagement.forms import AddScreenForm, AddGroup
from screenManagement.models import Screen, ScreenStatus, Group, GroupScreens, ScreenActivationKey, AspectRatio
# import the logging library

# Get an instance of a logger
from screenManagement.serializers import ScreenSerializer, GroupSerializer, AspectRatioSerializer


# Create your views here.


def default_screen_status():
    return ScreenStatus.objects.get(status_name__icontains='offline')


@transaction.atomic
@login_required
def upsert_group(request):
    """
    :param request.body='{'group_name', 'description', 'group_id', 'screens'}'
    :return: success, errors
    """
    posted_data = string_to_dict(request.body)
    success = False
    errors = []
    if request.method == 'POST':
        add_group_form = AddGroup(data=posted_data)
        if add_group_form.is_valid():
            user_details = get_userdetails(request)
            form_data = add_group_form.cleaned_data
            try:
                with transaction.atomic():
                    group_id = posted_data['group_id']
                    if group_id == -1:
                        group = Group(group_name=form_data.get('group_name'), organization=user_details.organization,
                                      created_by=user_details)
                    else:
                        group = Group.get_user_relevant_objects(user_details).get(group_id=group_id)
                        group.group_name = form_data.get('group_name')
                    group.description = form_data.get('description')
                    group.last_updated_by = user_details
                    group.save()
                    screens = posted_data.get('screens')
                    group_screen_id_list = []
                    for each_screen in screens:
                        group_screen_id = each_screen.get('group_screen_id')
                        if group_screen_id == -1:
                            screen_id = each_screen.get('screen_id')
                            screen = Screen.get_user_relevant_objects(user_details=user_details).get(screen_id=screen_id)
                            group_screen = GroupScreens.objects.create(screen=screen, group=group, created_by=user_details)
                            group_screen_id = group_screen.group_screen_id
                        group_screen_id_list.append(group_screen_id)
                    removed_group_screens = GroupScreens.objects.filter(group=group).exclude(
                        group_screen_id__in=group_screen_id_list)
                    removed_group_screens.delete()
                    success = True
            except Exception as e:
                debugFileLog.exception(e)
                errors = ['Error while adding the group details']
        else:
            debugFileLog.exception('Add/Edit Group Form is not valid')
            print add_group_form.errors
            errors = add_group_form.errors
    return ajax_response(success=success, errors=errors)


@transaction.atomic
@login_required
def delete_group(request):
    """
    :param request.body: '{'group_id': 1}'
    :return: success, errors
    """
    user_details = get_userdetails(request)
    posted_data = string_to_dict(request.body)
    group_id = int(posted_data.get('group_id'))
    success = False
    errors = []
    try:
        with transaction.atomic():
            user_content = Group.get_user_relevant_objects(user_details).get(group_id=group_id)
            user_content.delete()
            success = True
    except Exception as e:
        print "Exception is ", e
        error = "Error while deleting the group"
        print error
        errors.append(error)
    return ajax_response(success=success, errors=errors)


@transaction.atomic
@login_required
def upsert_screen(request):
    user_details = get_userdetails(request)
    posted_data = string_to_dict(request.body)
    success = False
    errors = []
    try:
        with transaction.atomic():
            screen_id = int(posted_data.get('screen_id'))
            if screen_id == -1:
                activation_key = posted_data.get('activation_key')
                try:
                    screen_activation_key = ScreenActivationKey.objects.get(activation_key=activation_key, in_use=False,
                                                                            verified=True)
                    screen = Screen(screen_name=posted_data.get('screen_name'), unique_device_key=screen_activation_key,
                                    activated_by=user_details)
                    screen.save()
                    screen_activation_key.in_use = True
                    screen_activation_key.save()
                except Exception as e:
                    print "Not a valid activation key"
                    print "Exception is ", e
                    return ajax_response(success=False, errors=['Not a valid activation key, contact support@blynq.in'])
            else:
                screen = Screen.get_user_relevant_objects(user_details).get(screen_id=screen_id)
            screen.screen_name = posted_data.get('screen_name')
            screen_size = posted_data.get('screen_size')
            if screen_size:
                screen.screen_size = int(screen_size)
            screen.address = posted_data.get('address')
            city = posted_data.get('city')
            if city:
                city_id = int(city.get('city_id'))
                screen.city_id = city_id
            else:
                screen.city = None
            screen.aspect_ratio = posted_data.get('aspect_ratio')
            screen.resolution = posted_data.get('resolution')
            screen.owned_by = user_details.organization
            screen.last_updated_by = user_details
            status = default_screen_status()
            screen.status = status
            screen.save()
            group_screen_id_list = []
            for group in posted_data.get('groups'):
                group_screen_id = group.get('group_screen_id')
                if group_screen_id:
                    group_screen_id = int(group_screen_id)
                else:
                    group_screen_id = -1
                if group_screen_id == -1:
                    group_entry = Group.get_user_relevant_objects(user_details).get(group_id=int(group.get('group_id')))
                    group_screen = GroupScreens.objects.create(group=group_entry, screen=screen, created_by=user_details)
                    group_screen_id = group_screen.group_screen_id
                group_screen_id_list.append(group_screen_id)

            removed_group_screens = GroupScreens.objects.filter(screen=screen).exclude(
                group_screen_id__in=group_screen_id_list)
            if removed_group_screens:
                removed_group_screens.delete()

            success_removal = True # remove_group_screens(screen=screen, group_screen_id_list=group_screen_id_list)
            if not success_removal:
                error = 'error while removing deleted groups from screen'
                debugFileLog.error(error)
                raise Exception(error)

            # Adding a calendar for each screen
            if not screen.screen_calendar:
                calendar = Calendar(name=screen.screen_name + str(screen.screen_id))
                calendar.save()
                screen.screen_calendar = calendar
                screen.save()
            # TODO: The above case only handles the PRIVATE businessType, add a check
            success = True
    except Exception as e:
        debugFileLog.exception(e)
        errors = ['Error while adding the screen details to database']
        success = False
    return ajax_response(success=success, errors=errors)


# TODO: Understand the difference between natural_key method and get_by_natural_key method in
# https://docs.djangoproject.com/en/1.9/topics/serialization/
def get_groups_json(request):
    debugFileLog.info("inside get_groups_json")
    user_details = get_userdetails(request)
    groups_data = Group.get_user_relevant_objects(user_details=user_details)
    json_data = GroupSerializer().serialize(groups_data, fields=('group_id', 'group_name', 'description', 'screens'))
    return obj_to_json_response(json_data)


def get_screens_json(request):
    user_details = get_userdetails(request)
    screen_data = Screen.get_user_relevant_objects(user_details)
    json_data = ScreenSerializer().serialize(screen_data,
                                             fields=('screen_id', 'screen_name', 'address', 'city',
                                                     'status', 'groups', 'screen_size', 'resolution'),
                                             use_natural_foreign_keys=True)
    return obj_to_json_response(json_data)


def get_city_options(request):
    city_data = CitySerializer().serialize(City.objects.all(), fields=('city_id', 'city_name'))
    return obj_to_json_response(city_data)


def routeToHome(request):
    return render(request, 'Home.html')


@login_required
def screen_index(request):
    context_dic = {'form': AddScreenForm(form_name='formAddScreen', scope_prefix='modalScreenDetailsObj')}
    return render(request, 'screen/screens.html', context_dic)


def group_index(request):
    context_dic = {'form': AddGroup(form_name='formGroup', scope_prefix='modalGroupDetailsObj')}
    return render(request, 'screen/groups.html', context_dic)


def get_aspect_ratios(request):
    json_data = AspectRatioSerializer().serialize(AspectRatio.objects.all())
    return obj_to_json_response(json_data)
