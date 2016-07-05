from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from authentication.forms import RequestQuoteForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from authentication.models import UserDetails, Organization, Role, PlayerUpdate
from blynq import settings
from blynq.settings import MEDIA_HOST
from customLibrary.views_lib import string_to_dict, ajax_response, get_userdetails, send_mail_blynq, obj_to_json_response, \
    debugFileLog, default_string_to_datetime
from scheduleManagement.models import Schedule
from screenManagement.models import Screen, ScreenActivationKey


# def register(request):
#     if request.user.is_authenticated():
#         return HttpResponseRedirect('homepage', request)
#     registered = False
#     context_dic = {}
#     if request.method == 'POST':
#         user_details_form = UserDetailsForm(data=request.POST)
#         if user_details_form.is_valid():
#             user_details = UserDetails.objects.create_user(username=user_details_form.cleaned_data['username'],
#                                                            first_name=user_details_form.cleaned_data['first_name'],
#                                                            last_name=user_details_form.cleaned_data['last_name'],
#                                                            email=user_details_form.cleaned_data['email'],
#                                                            password=user_details_form.cleaned_data['password'],
#                                                            organization=user_details_form.cleaned_data['organization'],
#                                                            mobile_number=user_details_form.cleaned_data['mobile_number'],
#                                                            role=user_details_form.cleaned_data['role']
#                                                            )
#             registered = True
#         else:
#             print 'Error in User Details Form'
#             print user_details_form.errors
#     else:
#         context_dic['user_details_form'] = UserDetailsForm()
#
#     context_dic['registered'] = registered
#     return render(request,'authentication/register.html', context_dic)


def login(request):
    context_dic ={}
    if request.user.is_authenticated():
        print 'authenticated'
        return HttpResponseRedirect(reverse('index_page'))
    else:
        if request.method == 'POST':
            success = False
            postedData = string_to_dict(request.body)
            username = postedData.get('username')
            password = postedData.get('password')
            # print username, password
            user = authenticate(username=username, password=password)
            if user:
                print "authenticate successfull"
                auth_login(request, user)
                success = True
                return ajax_response(success=success)
            else:
                return ajax_response(success = success)

    return render(request, 'authentication/login.html', context_dic)


@login_required
def divert_to_index_page(request, **kwargs):
    return render(request, 'masterLayout.html')


@login_required
def homePage(request):
    return render(request, 'Home.html')



def divertToLandingPage(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index_page', args=(request)))
    else:
        return render(request, 'landing_page_content.html')


def request_quote(request):
    posted_data = string_to_dict(request.body)
    success = False
    errors = []
    if request.method == 'POST':
        request_quote_form = RequestQuoteForm(data=posted_data)
        if request_quote_form.is_valid():
            try:
                request_quote_form.save()
                message = 'Name: ' + str(posted_data.get('name')) + '\n\n'
                message += 'E-mail: ' + str(posted_data.get('email')) + '\n\n'
                message += 'Mobile Number: ' + str(posted_data.get('mobile_number')) + '\n\n'
                message += 'Number of Devices: ' + str(posted_data.get('num_of_devices')) + '\n\n'
                message += 'Additional Details: ' + str(posted_data.get('additional_details')) + '\n\n'
                send_mail_blynq(subject='[Auto-Generated] Quote Requested', message=message)
                success = True
            except Exception as e:
                print "Exception is ", e
                error = "Error while saving the requested Quote"
                errors.append(error)
                print error
        else:
            error = "Request Quote form data is not valid"
            errors.append(error)
            print error
    return ajax_response(success=success, errors=errors)


@login_required
def organization_homepage_summary(request):
    debugFileLog.info("inside organization_homepage_summary")
    user_details = get_userdetails(request=request)
    context_dic = {}
    try:
        screen_count = Screen.get_user_relevant_objects(user_details=user_details).count()
        schedule_count = Schedule.get_user_relevant_objects(user_details=user_details).count()
        context_dic['screen_count'] = screen_count
        context_dic['schedule_count'] = schedule_count
        organization = user_details.organization
        context_dic['used_storage'] = organization.used_file_size
        context_dic['total_storage'] = organization.total_file_size_limit
    except Exception as e:
        print "Exception is ", e
        context_dic['used_storage'] = 0
        context_dic['total_storage'] = settings.STORAGE_LIMIT_PER_ORGANIZATION
    return obj_to_json_response(context_dic)


# def logout(request):
#     print 'I am in logout'
#     auth_logout(request)
#     return HttpResponse('User logged out successfully.')

#private methods

'''
def setSessionVar(request, status):
    request.session['userLoggedIn'] = status
'''

# TODO: Using tv remote to move slides.


@csrf_exempt
def get_player_update(request):
    debugFileLog.info("inside get_player_update")
    errors = []
    posted_data = string_to_dict(request.body)
    # the datetime format of last_received should be
    last_received = posted_data.get('last_received')
    unique_device_key = posted_data.get('device_key')
    last_received_datetime = default_string_to_datetime(last_received)
    player_json={'is_update_available': False, 'url': None}
    try:
        screen = ScreenActivationKey.objects.get(activation_key=unique_device_key, verified=True)
        updates = PlayerUpdate.objects.filter(uploaded_time__gt=last_received_datetime)
        if updates:
            player_json['is_update_available'] = True
            player_json['url'] = MEDIA_HOST + updates[0].executable.url
    except ScreenActivationKey.DoesNotExist:
        debugFileLog.exception('Screen activation key does not exist')
    except Exception as e:
        debugFileLog.exception(e)
    return obj_to_json_response(player_json)