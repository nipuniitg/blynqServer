from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from JsonTestData import TestDataClass
from django.http import JsonResponse

from authentication.models import UserDetails, Organization, Address
from screenManagement.forms import AddScreenForm, AddScreenLocation, AddScreenSpecs, AddGroup
from screenManagement.models import Screen, ScreenStatus, ScreenSpecs, Group


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
def add_screen(request):
    context_dic = {}
    success = False
    if request.method == 'POST':
        add_screen_form = AddScreenForm(data=request.POST)
        if add_screen_form.is_valid():
            try:
                user_details = UserDetails.objects.get(username=request.user.username)
                organization = user_details.organization
            except:
                organization = default_organization()
            form_data = add_screen_form.cleaned_data
            try:
                status = default_screen_status()
                screen = Screen.objects.create(screen_name=form_data.get('screen_name'),
                                               specifications=form_data.get('specifications'),
                                               location=form_data.get('location'),
                                               owned_by=organization,
                                               status=status,
                                               )
                for group in form_data.get('groups'):
                    screen.groups.add(group)
                # TODO: The above case only handles the PRIVATE businessType, add a check
                # OrganizationScreen.objects.create(organization=organization,
                #                                   screen=screen,
                #                                   )
                success = True
                success_message = "The Screen has been successfully Added."
                context_dic['success_message'] = success_message
            except:
                print 'Error while adding the screen to database'
        else:
            print 'Add Screen Form is not valid'
            print add_screen_form.errors
    else:
        context_dic['form'] = AddScreenForm()
        # TODO: Not able to unselect the Group field once selected, fix this issue in the frontend.
    context_dic['title'] = "Add Screen"
    context_dic['submitButton'] = "Submit"
    context_dic['success'] = success
    context_dic['target'] = reverse('add_screen')
    print context_dic
    return render(request,'Shared/displayForm.html', context_dic)


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
                                             organization=organization
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
        context_dic['form'] = AddGroup()
    context_dic['title'] = "Create Group"
    context_dic['submitButton'] = "Submit"
    context_dic['success'] = success
    context_dic['target'] = reverse('add_group')
    return render(request,'Shared/displayForm.html', context_dic)

@login_required
def screen_index(request):
    return render(request,'screen/screens.html')


def group_index(request):
    return render(request, 'screen/groups.html')


def routeToHome(request):
    return render(request, 'Home.html')


def testScreen(request):
    return render(request,'testTemplate.html')


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
    data = serializers.serialize("json", Group.objects.all(), fields=('group_name', 'description'))
    return HttpResponse(data, content_type='application/json')


def get_screens_json(request):
    user_details, organization = user_and_organization(request)
    data = serializers.serialize("json", Screen.objects.filter( owned_by=organization ), fields=('screen_id', 'screen_name', 'address', 'status', 'groups', 'screen_size', 'resolution'), use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return HttpResponse(data, content_type='application/json')


def get_screen(request, screen_id=1):
    print screen_id
    data = serializers.serialize("json", Screen.objects.filter(pk=screen_id), use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return HttpResponse(data, content_type='application/json')