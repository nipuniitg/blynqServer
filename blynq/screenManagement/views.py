from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render
from schedule.models import Calendar

from authentication.models import Address
from customLibrary.views_lib import ajax_response, get_userdetails, string_to_dict, list_to_json, debugFileLog
from scheduleManagement.models import ScheduleScreens
from screenManagement.forms import AddScreenForm, AddScreenLocation, AddScreenSpecs, AddGroup
from screenManagement.models import Screen, ScreenStatus, ScreenSpecs, Group, GroupScreens, ScreenActivationKey

# import the logging library

# Get an instance of a logger
from screenManagement.serializers import ScreenSerializer, GroupSerializer


# Create your views here.


def default_screen_status():
    return ScreenStatus.objects.get(status_name__icontains='offline')


@login_required
def add_group(request):
    debugFileLog.info("inside Add Group")
    context_dic = {}
    success = False
    if request.method == 'POST':
        add_group_form = AddGroup(data=request.POST)
        if add_group_form.is_valid():
            form_data = add_group_form.cleaned_data
            try:
                user_details = get_userdetails(request)
                group = Group.objects.create(group_name=form_data.get('group_name'),
                                             description=form_data.get('description'),
                                             created_by=user_details,
                                             )
                success = True
                success_message = "Group %s have been successfully Added." % form_data.get('group_name')
                context_dic['success_message'] = success_message
            except Exception as e:
                print "Exception is ", e
                print 'Error while adding the new group to database'
        else:
            print 'Add Group Form is not valid'
            print add_group_form.errors
    else:
        context_dic['form'] = AddGroup(form_name='form', scope_prefix='modalGroupDetailsObj')
    context_dic['title'] = "Create Group"
    context_dic['submitButton'] = "Submit"
    context_dic['success'] = success
    context_dic['target'] = reverse('add_group')
    return render(request, 'Shared/displayForm.html', context_dic)


def insert_group_screen(screen, group):
    group_schedules = ScheduleScreens.objects.filter(screen__isnull=True, group=group)
    try:
        for each_group_schedule in group_schedules:
            screen_event = each_group_schedule.event
            screen_event.pk = None
            screen_event.calendar = screen.screen_calendar
            screen_event.save()
            ScheduleScreens.object.create(screen=screen, schedule=each_group_schedule.schedule,
                                          group=group, event=screen_event)
    except Exception as e:
        print "Exception is ", e
        return False
    return True


# This function is to either remove groups from screens or screens from groups and remove relevant entries from the
# ScheduleScreens table
def remove_group_screens(screen=None, group=None, group_screen_id_list=[]):
    print "inside remove_group_screens"
    # Only one of the screen/group should be None
    if screen:
        # Remove groups not in the group_screen_id_list
        removed_group_screens = GroupScreens.objects.filter(screen=screen).exclude(
            group_screen_id__in=group_screen_id_list)
    elif group:
        # Remove screens deleted from the group
        removed_group_screens = GroupScreens.objects.filter(group=group).exclude(
            group_screen_id__in=group_screen_id_list)
    else:
        removed_group_screens = []
    try:
        for each_group_screen in removed_group_screens:
            schedule_screens = ScheduleScreens.objects.filter(group=each_group_screen.group,
                                                              screen=each_group_screen.screen)
            for each_schedule_screen in schedule_screens:
                event = each_schedule_screen.event
                if event:
                    if event.rule:
                        event.rule.delete()
                    event.delete()
            if schedule_screens:
                rows_deleted = schedule_screens.delete()
        if removed_group_screens:
            removed_group_screens.delete()
    except Exception as e:
        print "Exception is ", e
        return False
    return True


@login_required
def upsert_group(request):
    transaction.set_autocommit(False)
    posted_data = string_to_dict(request.body)
    success = False
    errors = []
    if request.method == 'POST':
        add_group_form = AddGroup(data=posted_data)
        if add_group_form.is_valid():
            user_details = get_userdetails(request)
            form_data = add_group_form.cleaned_data
            try:
                group_id = posted_data['group_id']
                if group_id == -1:
                    group = Group(group_name=form_data.get('group_name'), organization=user_details.organization,
                                  created_by=user_details)
                else:
                    group = Group.get_user_relevant_objects(user_details).get(group_id=group_id)
                    group.group_name = form_data.get('group_name')
                group.description = form_data.get('description')
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
                        success_insert = insert_group_screen(group=group, screen=screen)
                        if not success_insert:
                            error = 'error while removing inserting screens to group'
                            print error
                            transaction.rollback()
                            return ajax_response(success=success_insert, errors=[error])
                    group_screen_id_list.append(group_screen_id)

                success_removal = remove_group_screens(group=group, group_screen_id_list=group_screen_id_list)
                if not success_removal:
                    error = 'error while removing deleted screens from group'
                    print error
                    transaction.rollback()
                    return ajax_response(success=success_removal, errors=[error])

                success = True
            except Exception as e:
                print "Exception is ", e
                errors = ['Error while adding the group details to database']
                print errors[0]
        else:
            print 'Add/Edit Group Form is not valid'
            print add_group_form.errors
            errors = add_group_form.errors
    if success:
        transaction.commit()
    else:
        transaction.rollback()
    return ajax_response(success=success, errors=errors)


def delete_group(request):
    user_details = get_userdetails(request)
    posted_data = string_to_dict(request.body)
    group_id = int(posted_data.get('group_id'))
    success = False
    errors = []
    try:
        user_content = Group.get_user_relevant_objects(user_details).get(group_id=group_id)
        user_content.delete()
        success = True
    except Exception as e:
        print "Exception is ", e
        error = "Error while deleting the group"
        print error
        errors.append(error)
    return ajax_response(success=success, errors=errors)


def activation_key_valid(request):
    user_details = get_userdetails(request)
    posted_data = string_to_dict(request.body)
    activation_key = posted_data.get('activation_key')
    success = False
    errors = []
    try:
        screen_activation_key = ScreenActivationKey.objects.get(activation_key=activation_key, in_use=False)
        success = True
    except ScreenActivationKey.DoesNotExist:
        errors = ['Invalid activation key, try another or contact support']
        success = False
    return ajax_response(success=success, errors=errors)


# Replace upsert_screen with upsert_screen1 after Prasanth implements the AddScreenForm
@login_required
def upsert_screen(request):
    transaction.set_autocommit(False)
    user_details = get_userdetails(request)
    posted_data = string_to_dict(request.body)
    success = False
    errors = []
    try:
        screen_id = int(posted_data.get('screen_id'))
        if screen_id == -1:
            activation_key = posted_data.get('activation_key')
            try:
                screen_activation_key = ScreenActivationKey.objects.get(activation_key=activation_key, in_use=False)
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
            screen = Screen.objects.get(screen_id=screen_id)
        screen.screen_size = int(posted_data.get('screen_size'))
        screen.address = posted_data.get('address')
        city_id = int(posted_data.get('city_id'))
        if city_id != -1:
            screen.city_id = posted_data.get('city_id')
        screen.aspect_ratio = posted_data.get('aspect_ratio')
        screen.resolution = posted_data.get('resolution')
        screen.owned_by = user_details.organization
        status = default_screen_status()
        screen.status = status
        screen.save()
        group_screen_id_list = []
        for group in posted_data.get('groups'):
            group_screen_id = int(group.get('group_screen_id'))
            if group.group_screen_id == -1:
                group_entry = Group.objects.get(group_id=int(group.get('group_id')))
                group_screen = GroupScreens.objects.create(group=group_entry, screen=screen, created_by=user_details)
                group_screen_id = group.group_screen_id
                success_insert = insert_group_screen(screen=screen, group=group_entry)
                if not success_insert:
                    error = 'error while inserting group to screen'
                    print error
                    transaction.rollback()
                    return ajax_response(success=success_insert, errors=[error])
            group_screen_id_list.append(group_screen_id)

        success_removal = remove_group_screens(screen=screen, group_screen_id_list=group_screen_id_list)
        if not success_removal:
            error = 'error while removing deleted groups from screen'
            print error
            transaction.rollback()
            return ajax_response(success=success_removal, errors=[error])

        # Adding a calendar for each screen
        if not screen.screen_calendar:
            calendar = Calendar(name=screen.screen_name + str(screen.screen_id))
            calendar.save()
            screen.screen_calendar = calendar
            screen.save()
        # TODO: The above case only handles the PRIVATE businessType, add a check
        success = True
    except Exception as e:
        print "Exception is ", e
        errors = ['Error while adding the screen details to database']
        print errors[0]
        success = False
    if success:
        transaction.commit()
    else:
        transaction.rollback()
    return ajax_response(success=success, errors=errors)


# TODO: Understand the difference between natural_key method and get_by_natural_key method in
# https://docs.djangoproject.com/en/1.9/topics/serialization/
def get_groups_json(request):
    debugFileLog.info("inside get_groups_json")
    user_details = get_userdetails(request)
    groups_data = Group.get_user_relevant_objects(user_details=user_details)
    json_data = GroupSerializer().serialize(groups_data, fields=('group_id', 'group_name', 'description', 'screens'))
    return list_to_json(json_data)


def get_screens_json(request):
    user_details = get_userdetails(request)
    screen_data = Screen.get_user_relevant_objects(user_details)
    json_data = ScreenSerializer().serialize(screen_data,
                                             fields=('screen_id', 'screen_name', 'address', 'city',
                                                     'status', 'groups', 'screen_size', 'resolution'),
                                             use_natural_foreign_keys=True)
    return list_to_json(json_data)


def get_selectable_screens_json(request, group_id=-1):
    user_details = get_userdetails(request)
    screen_data = Screen.get_user_relevant_objects(user_details).exclude(groups__pk=group_id)
    json_data = ScreenSerializer().serialize(screen_data, fields=('screen_id', 'screen_name', 'address', 'city', 'status',
                                                   'groups', 'screen_size', 'resolution', 'group_screen_id'),
                                           use_natural_foreign_keys=True)
    return list_to_json(json_data)


def get_selectable_groups_json(request, screen_id=-1):
    user_details = get_userdetails(request)
    groups_data = Group.objects.filter(organization=user_details.organization).exclude(screen__pk=screen_id)
    json_data = GroupSerializer().serialize(groups_data, fields=('group_id', 'group_name', 'group_screen_id'))
    return list_to_json(json_data)


# Unused functions
@login_required
def add_screen_location(request):
    context_dic = {}
    success = False
    if request.method == 'POST':
        user_details = get_userdetails(request)
        screen_location_form = AddScreenLocation(data=request.POST)
        if screen_location_form.is_valid():
            try:
                user_details = get_userdetails(request)
            except Exception as e:
                print "Exception is ", e
                print 'Error: username %s does not exist' % str(request.user.username)
            form_data = screen_location_form.cleaned_data
            try:
                location = Address.objects.create(building_name=form_data.get('building_name'),
                                                  address_line1=form_data.get('address_line1'),
                                                  address_line2=form_data.get('address_line2'),
                                                  area=form_data.get('area'),
                                                  landmark=form_data.get('landmark'),
                                                  city=form_data.get('city'),
                                                  pincode=form_data.get('pincode'),
                                                  added_by=user_details
                                                  )
                # TODO: Add an entry of the above screen in the OrganizationScreen
                # TODO: The above case only handles the PRIVATE businessType
                # OrganizationScreen.objects.create(organization=organization,
                #                                   screen=screen,
                #                                   )
                success = True
                success_message = "The address of location has been successfully Added."
                context_dic['success_message'] = success_message
            except Exception as e:
                print "Exception is ", e
                print 'Error while adding the screen location to database'
        else:
            print 'Add Screen location Form is not valid'
            print screen_location_form.errors
    else:
        context_dic['form'] = AddScreenLocation()
    context_dic['title'] = "Add Screen Location"
    context_dic['submitButton'] = "Submit"
    context_dic['success'] = success
    context_dic['target'] = reverse('add_screen_location')
    return render(request, 'Shared/displayForm.html', context_dic)


@login_required
def add_screen_specs(request):
    context_dic = {}
    success = False
    if request.method == 'POST':
        screen_specs_form = AddScreenSpecs(data=request.POST)
        if screen_specs_form.is_valid():
            form_data = screen_specs_form.cleaned_data
            try:
                screen_specs = ScreenSpecs.objects.create(brand=form_data.get('brand'),
                                                          model_num=form_data.get('model_num'),
                                                          weight=form_data.get('weight'),
                                                          dimensions=form_data.get('dimensions'),
                                                          resolution=form_data.get('resolution'),
                                                          display_type=form_data.get('display_type'),
                                                          screen_size=form_data.get('screen_size'),
                                                          aspect_ratio=form_data.get('aspect_ratio'),
                                                          contrast_ratio=form_data.get('contrast_ratio'),
                                                          wattage=form_data.get('wattage'),
                                                          additional_details=form_data.get('additional_details')
                                                          )
                success = True
                success_message = "The specifications of the screen have been successfully Added."
                context_dic['success_message'] = success_message
            except Exception as e:
                print "Exception is ", e
                print 'Error while adding the screen specifications to database'
        else:
            print 'Add Screen specifications Form is not valid'
            print screen_specs_form.errors
    else:
        context_dic['form'] = AddScreenSpecs()
    context_dic['title'] = "Add Screen Specifications"
    context_dic['submitButton'] = "Submit"
    context_dic['success'] = success
    context_dic['target'] = reverse('add_screen_specs')
    return render(request, 'Shared/displayForm.html', context_dic)


def routeToHome(request):
    return render(request, 'Home.html')


@login_required
def screen_index(request):
    context_dic = {}
    context_dic['form'] = AddScreenForm(form_name='formAddScreen', scope_prefix='modalScreenDetailsObj')
    return render(request, 'screen/screens.html', context_dic)


def group_index(request):
    context_dic = {}
    context_dic['form'] = AddGroup(form_name='formGroup', scope_prefix='modalGroupDetailsObj')
    return render(request, 'screen/groups.html', context_dic)
