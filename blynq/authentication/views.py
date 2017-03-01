import datetime
from django.contrib.auth.models import User

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from authentication.forms import RequestQuoteForm
from authentication.models import Organization, UserDetails, Role
from blynq import settings
from customLibrary.custom_settings import PLAYER_INACTIVE_THRESHOLD
from customLibrary.views_lib import string_to_dict, ajax_response, get_userdetails, send_mail_blynq, obj_to_json_response, \
    debugFileLog, mail_exception
from scheduleManagement.models import Schedule
from screenManagement.models import Screen


def create_organization(organization_name):
    organization = None
    if organization_name:
        try:
            organization = Organization.objects.create(organization_name=organization_name)
        except Exception as e:
            debugFileLog.error('Error while creating new organization %s during sign up' % str(organization_name))
            mail_exception(str(e))
    else:
        mail_exception('Empty or Null organization name')
    return organization


def register(request):
    context_dic = {'registered': False}
    try:
        if request.user.is_authenticated():
            return HttpResponseRedirect('homepage', request)
        if request.method == 'POST':
            posted_data = string_to_dict(request.body)
            username = posted_data.get('username')
            if not username:
                errors = ['Invalid username']
            else:
                try:
                    user = User.objects.get(username=username)
                    errors = ['Username already exists']
                except Exception as e:
                    user = User.objects.create_user(username=username, first_name=posted_data.get('first_name'),
                                                    last_name=posted_data.get('last_name'), email=posted_data.get('email'),
                                                    password=posted_data.get('password'))
                    if user:
                        organization_name = posted_data.get('organization_name')
                        if not organization_name:
                            organization_name = username
                        new_organization = create_organization(organization_name=organization_name)
                        try:
                            user_details = UserDetails.objects.create(user=user, organization=new_organization,
                                                                      role=Role.default_role(),
                                                                      mobile_number=str(posted_data.get('mobile_number')))
                            context_dic['registered'] = True
                        except Exception as e:
                            error = 'Unable to create UserDetails for username %s' % username
                            mail_exception(error+str(e))
    except Exception as e:
        mail_exception('Some error while Sign Up' + str(e) + str(request.body))
    if context_dic['registered']:
        send_mail_blynq(to=['prasanth@blynq.in'], subject="New User registered", message=str(request.body))
    else:
        context_dic['errors'] = 'Unable to process your sign up request. Our support team will contact you in sometime.'
    return ajax_response(success=context_dic['registered'])


def username_availability(request):
    posted_data = string_to_dict(request.body)
    context_dic = {'username_available': False}
    username = posted_data.get('username')
    if username:
        try:
            user = User.objects.get(username=username)
            if user:
                context_dic['username_available'] = False
            else:
                context_dic['username_available'] = True
        except Exception as e:
            context_dic['username_available'] = True
    return JsonResponse(context_dic, safe=False)


def login(request):
    context_dic ={}
    if request.user.is_authenticated():
        debugFileLog.info('authenticated')
        return HttpResponseRedirect(reverse('index_page'))
    else:
        if request.method == 'POST':
            success = False
            posted_data = string_to_dict(request.body)
            username = posted_data.get('username')
            password = posted_data.get('password')
            # print username, password
            user = authenticate(username=username, password=password)
            if user:
                debugFileLog.info("authenticate successful")
                auth_login(request, user)
                success = True
                return ajax_response(success=success)
            else:
                return ajax_response(success=success)
    return render(request, 'index.html', context_dic)


def get_profile_details(request):
    context_dic = {}
    try:
        user_details = get_userdetails(request)
        context_dic['first_name'] = user_details.user.first_name
        context_dic['last_name'] = user_details.user.last_name
        context_dic['email'] = user_details.user.email
        context_dic['mobile_number'] = user_details.mobile_number
    except Exception as e:
        mail_exception(exception=e)
    return obj_to_json_response(context_dic)


def update_user_details(request):
    errors = []
    try:
        user_details = get_userdetails(request)
        user = user_details.user
        posted_data = string_to_dict(request.body)
        user.first_name = posted_data.get('first_name')
        user.last_name = posted_data.get('last_name')
        user.email = posted_data.get('email')
        user_details.mobile_number = posted_data.get('mobile_number')
        user.save()
        user_details.save()
        success = True
    except Exception as e:
        debugFileLog.error('Request body is ' + str(request.body))
        mail_exception(exception=e)
        errors = ['Improper User details']
        success = False
    return ajax_response(success=success, errors=errors)


def change_password(request):
    errors = []
    try:
        user_details = get_userdetails(request)
        posted_dict = string_to_dict(request.body)
        current_password = posted_dict.get('current_password')
        user = authenticate(username=user_details.user.username, password=current_password)
        if not user:
            return ajax_response(success=False, errors=['Wrong current password, please try again'])
        new_password = posted_dict.get('new_password')
        reenter_password = posted_dict.get('reenter_new_password')
        if new_password:
            if new_password != reenter_password:
                return ajax_response(success=False, errors=['New Password mismatch'])
            user = user_details.user
            user.set_password(new_password)
            user.save()
            success = True
        else:
            success = False
            errors = ['New password shouldn\'t be empty']
    except Exception as e:
        success = False
        errors = ['Password change unsuccessful']
        debugFileLog.error('Request body is ' + str(request.body))
        mail_exception(exception=e)
    return ajax_response(success=success, errors=errors)


@csrf_exempt
def create_new_client(request):
    """
    :param request: partner_key, client_name
    :return:
    """
    success = False
    errors = []
    try:
        posted_data = string_to_dict(request.body)
        partner_key = posted_data.get('partner_key')
        partner = Organization.objects.get(secret_key=partner_key)
        client_name = posted_data.get('client_name')
        if not client_name:
            return ajax_response(success=False, errors=['Improper new organization name details'])
        client_org = Organization.objects.create(organization_name=client_name, parent=partner, use_blynq_banner=False)
        client_key = client_org.secret_key
        # Comment above two lines and uncomment below two lines if the partner wants to generate own key for the client
        # client_key = posted_data.get('client_key')
        # client_org = Organization.objects.create(organization_name=client_name, parent=partner, client_key=client_key)
        client_userdetails = client_org.get_or_create_userdetails()
        if not client_userdetails:
            mail_exception(exception='',
                           subject='Not able to create userdetails for organization %s' % client_org.organization_name)
            return ajax_response(success=success, errors=['Not able to create client user credentials'])
        else:
            return ajax_response(success=True, obj_dict={'client_key': client_key})
    except (Organization.MultipleObjectsReturned, Organization.DoesNotExist) as e:
        mail_exception(exception=e, subject='Received exception while creating new client for partner')
        errors = ['Improper details, please contact support']
    except Exception as e:
        mail_exception(exception=e, subject='Received exception while creating new client for partner')
        errors = ['There is an error processing your request, please contact support']
    return ajax_response(success=success, errors=errors)


@csrf_exempt
def partner_login(request):
    success = False
    if request.method == 'GET':
        try:
            partner_key = request.GET['partner_key']
            client_key = request.GET['client_key']
            partner = Organization.objects.get(secret_key=partner_key)
            client = Organization.objects.get(secret_key=client_key, parent=partner)
            user_details = client.get_or_create_userdetails()
            if not user_details:
                return ajax_response(success=False)
            user = authenticate(username=user_details.user.username, password=client_key)
            if user:
                debugFileLog.info("partner %s authentication successful for client %s " % (partner.organization_name,
                                                                                           client.organization_name))
                auth_login(request, user)
                success = True
                return divert_to_index_page(request)
            else:
                debugFileLog.error(str(request.GET))
                mail_exception(exception='Not able to automatically authenticate for partner')
                return ajax_response(success=success)
        except Exception as e:
            mail_exception(exception=e, subject='Error with partner login %s' % str(request.GET))
    else:
        mail_exception(exception='Partner sending post request instead of get', subject='Error with partner login')
    return ajax_response(success, errors=['Login failed, please try again or contact support'])


def blynq_banner_usage(request):
    use_blynq_banner = True
    try:
        user_details = get_userdetails(request)
        use_blynq_banner = user_details.organization.use_blynq_banner
    except Exception as e:
        mail_exception(exception=e, subject='Received exception in fetch_blynq_banner')
    return use_blynq_banner


@login_required
def divert_to_index_page(request, **kwargs):
    from paymentManagement.views import payment_warning_dict
    context_dic = payment_warning_dict(request)
    context_dic['use_blynq_banner'] = blynq_banner_usage(request)
    if context_dic.get('suspend_access'):
        return render(request, 'payment_due.html', context_dic)
    else:
        return render(request, 'masterLayout.html', context_dic)


@login_required
def homePage(request):
    return render(request, 'Home.html')


def divertToLandingPage(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index_page', args=(request)))
    else:
        return render(request, 'index.html')


def request_quote(request):
    success = False
    errors = []
    try:
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
                    mail_exception(exception=e)
                    error = "Error while saving the requested Quote"
                    errors.append(error)
            else:
                error = "Request Quote form data is not valid"
                debugFileLog.exception(error)
                errors.append(error)
    except Exception as e:
        debugFileLog.error('request body is ' + str(request.body))
        mail_exception(e)
    return ajax_response(success=success, errors=errors)


@login_required
def organization_homepage_summary(request):
    debugFileLog.info("inside organization_homepage_summary")
    user_details = get_userdetails(request=request)
    context_dic = {}
    try:
        total_screen_count = Screen.get_user_relevant_objects(user_details=user_details).count()
        minimum_last_active_time = timezone.now() - datetime.timedelta(seconds=PLAYER_INACTIVE_THRESHOLD)
        active_screen_count = Screen.get_user_relevant_objects(user_details=user_details).filter(
            last_active_time__gte=minimum_last_active_time).count()
        schedule_count = Schedule.get_user_relevant_objects(user_details=user_details).count()
        context_dic['total_screen_count'] = total_screen_count
        context_dic['active_screen_count'] = active_screen_count
        context_dic['inactive_screen_count'] = total_screen_count - active_screen_count
        context_dic['schedule_count'] = schedule_count
        organization = user_details.organization
        context_dic['used_storage'] = organization.used_file_size
        context_dic['total_storage'] = organization.total_file_size_limit
    except Exception as e:
        mail_exception(exception=e)
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
