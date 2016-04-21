from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from JsonTestData import TestDataClass
from django.http import JsonResponse
import json

from authentication.models import UserDetails, Organization, Address
from screenManagement.forms import AddScreenForm, AddScreenLocation, AddScreenSpecs, AddGroup
from screenManagement.models import Screen, ScreenStatus, ScreenSpecs, Group
from screenManagement.serializers import FlatJsonSerializer as json_serializer

# Create your views here.


def default_organization():
    return Organization.objects.all()[0]


def default_userdetails():
    return UserDetails.objects.all()[0]


def default_screen_status():
    return ScreenStatus.objects.get(status_name__icontains='offline')


def user_and_organization(request):
    user_details = UserDetails.objects.get(username=request.user.username)
    organization = user_details.organization
    # user_details = default_userdetails()
    # organization = default_organization()
    return user_details, organization


@login_required
def add_group(request):
    context_dic = {}
    success = False
    if request.method == 'POST':
        add_group_form = AddGroup(data=request.POST)
        if add_group_form.is_valid():
            form_data = add_group_form.cleaned_data
            try:
                user_details, organization = user_and_organization(request)
                group = Group.objects.create(group_name=form_data.get('group_name'),
                                             description=form_data.get('description'),
                                             created_by=user_details,
                                             )
                success = True
                success_message = "Group %s have been successfully Added." % form_data.get('group_name')
                context_dic['success_message'] = success_message
            except:
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
    return render(request,'Shared/displayForm.html', context_dic)


@login_required
def upsert_group(request):
    context_dic = {}
    json_obj = json.loads(request.body)
    success = False
    errors = []
    if request.method == 'POST':
        add_group_form = AddGroup(data=json_obj)
        if add_group_form.is_valid():
            user_details, organization = user_and_organization(request)
            form_data = add_group_form.cleaned_data
            try:
                group_id = json_obj['group_id']
                if group_id == -1:
                    group = Group(group_name=form_data.get('group_name'), created_by=user_details)
                else:
                    group = Group.objects.get(group_id=group_id)
                    group.group_name = form_data.get('group_name')
                group.description = form_data.get('description')
                group.save()
                success = True
            except:
                errors = ['Error while adding the group details to database']
                print errors[0]
        else:
            print 'Add/Edit Group Form is not valid'
            print add_group_form.errors
            errors = add_group_form.errors
    context_dic['success'] = success
    context_dic['errors'] = errors
    return JsonResponse(context_dic, safe=False)


@login_required
def upsert_screen(request):
    context_dic = {}
    json_obj = json.loads(request.body)
    success = False
    errors = []
    if request.method == 'POST':
        add_screen_form = AddScreenForm(data=json_obj)
        if add_screen_form.is_valid():
            user_details, organization = user_and_organization(request)
            form_data = add_screen_form.cleaned_data
            try:
                # TODO: The logic for activation_key is pending and update the fields activated_by and activated_on
                status = default_screen_status()
                screen_id = json_obj['screen_id']
                if screen_id == -1:
                    screen = Screen(screen_name=form_data.get('screen_name'))
                else:
                    screen = Screen.objects.get(screen_id=screen_id)
                    screen.screen_name = form_data.get('screen_name')
                screen.screen_size = form_data.get('screen_size')
                screen.activation_key=form_data.get('activation_key')
                screen.address=form_data.get('address')
                screen.aspect_ratio=form_data.get('aspect_ratio')
                screen.resolution=form_data.get('resolution')
                screen.owned_by=organization
                screen.status=status
                screen.save()
                for group in json_obj.get('groups'):
                    group_entry = Group.objects.get(group_id=group.get('group_id'))
                    screen.groups.add(group_entry)
                # TODO: The above case only handles the PRIVATE businessType, add a check
                success = True
            except:
                errors = ['Error while adding the screen details to database']
                print errors[0]
        else:
            print 'Add/Edit Screen Form is not valid'
            print add_screen_form.errors
            errors = add_screen_form.errors
    context_dic['success'] = success
    context_dic['errors'] = errors
    return JsonResponse(context_dic, safe=False)

@login_required
def add_screen_location(request):
    context_dic = {}
    success = False
    if request.method == 'POST':
        screen_location_form = AddScreenLocation(data=request.POST)
        if screen_location_form.is_valid():
            try:
                user_details = UserDetails.objects.get(username=request.user.username)
            except:
                print 'Error: username %s does not exist' % str(request.user.username)
                user_details = default_userdetails()
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
            except:
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
    return render(request,'Shared/displayForm.html', context_dic)


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
            except:
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
    return render(request,'Shared/displayForm.html', context_dic)


@login_required
def screen_index(request):
    context_dic = {}
    context_dic['form'] = AddScreenForm(form_name='formAddScreen', scope_prefix='modalScreenDetailsObj')
    return render(request,'screen/screens.html', context_dic)


def group_index(request):
    context_dic ={}
    context_dic['form'] = AddGroup(form_name='formGroup', scope_prefix='modalGroupDetailsObj')
    return render(request, 'screen/groups.html', context_dic)


def routeToHome(request):
    return render(request, 'Home.html')


def getScreensJson(request):
    print('I m in view')
    classObj = TestDataClass()
    screens = classObj.getScreenTestData()
    return JsonResponse(screens, safe=False)


def getGroupsJson(request):
    classObj = TestDataClass()
    groups = classObj.getGroupsTestData()
    return JsonResponse(groups,safe=False)


# TODO: Understand the difference between natural_key method and get_by_natural_key method in
# https://docs.djangoproject.com/en/1.9/topics/serialization/
def get_groups_json(request):
    user_details, organization = user_and_organization(request)
    groups_data = Group.objects.filter(created_by__organization=organization)
    # json_data = serializers.serialize("json", groups_data, fields=('group_id','group_name', 'description', 'screen'))
    json_data = json_serializer().serialize(groups_data, fields=('group_id','group_name', 'description', 'screen'))
    return HttpResponse(json_data, content_type='application/json')


def get_screens_json(request):
    user_details, organization = user_and_organization(request)
    screen_data = Screen.objects.filter(owned_by=organization)
    json_data = json_serializer().serialize(screen_data, fields=('screen_id', 'screen_name', 'address', 'status',
                                                                 'groups', 'screen_size', 'resolution'))
    return HttpResponse(json_data, content_type='application/json')


def get_selectable_screens_json(request, group_id=-1):
    user_details, organization = user_and_organization(request)
    screen_data = Screen.objects.filter(owned_by=organization).exclude(groups__pk=group_id)
    json_data = json_serializer().serialize(screen_data, fields=('screen_id', 'screen_name', 'address', 'status',
                                                                 'groups', 'screen_size', 'resolution'))
    return HttpResponse(json_data, content_type='application/json')


def get_selectable_groups_json(request, screen_id=-1):
    user_details, organization = user_and_organization(request)
    groups_data = Group.objects.filter(created_by__organization=organization).exclude(screen__pk=screen_id)
    json_data = json_serializer().serialize(groups_data, fields=('group_id', 'group_name'))
    return HttpResponse(json_data, content_type='application/json')
