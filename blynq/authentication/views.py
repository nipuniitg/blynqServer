from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from authentication.forms import RequestQuoteForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from authentication.models import UserDetails, Organization, Role
from blynq import settings
from customLibrary.views_lib import string_to_dict, ajax_response, get_userdetails, send_mail_blynq
from scheduleManagement.models import Schedule
from screenManagement.models import Screen


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
        return HttpResponseRedirect(reverse('homepage', args=(request)))
    else:
        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            # print username, password
            user = authenticate(username=username, password=password)
            if user:
                print "authenticate successfull"
                auth_login(request, user)
                return HttpResponseRedirect(reverse('homepage'))
            else:
                return HttpResponse('Invalid Login Details')

    return render(request, 'authentication/login.html', context_dic)


@login_required
def homePage(request):
    return render(request, 'Home.html')


def divertToLandingPage(request):
    return render(request, 'landing_page_content.html')


@login_required
def getPartailtemplate(request, template_name):
    path = 'scheduleManagement/'
    extn = '.html'
    return render(request, (path+template_name+extn))


def request_quote(request):
    posted_data = string_to_dict(request.body)
    success = False
    errors = []
    if request.method == 'POST':
        request_quote_form = RequestQuoteForm(data=posted_data)
        if request_quote_form.is_valid():
            try:
                request_quote_form.save()
                message = 'Name: ' + posted_data.get('name') + '\n'
                message += 'E-mail: ' + posted_data.get('email') + '\n'
                message += 'Mobile Number: ' + posted_data.get('mobile_number')
                message += 'Number of Devices: ' + posted_data.get('num_of_devices')
                message += 'Additional Details: ' + posted_data.get('additional_details')
                send_mail_blynq(subject='Quote Requested', message=message)
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
    print "inside organization_homepage_summary"
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
    return context_dic


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


