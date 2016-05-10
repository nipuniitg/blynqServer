from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from authentication.forms import UserDetailsForm, RequestQuoteForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from authentication.models import UserDetails, Organization, Role
from customLibrary.views_lib import string_to_dict, ajax_response


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('homepage', request)
    registered = False
    context_dic = {}
    if request.method == 'POST':
        user_details_form = UserDetailsForm(data=request.POST)
        if user_details_form.is_valid():
            user_details = UserDetails.objects.create_user(username=user_details_form.cleaned_data['username'],
                                                           first_name=user_details_form.cleaned_data['first_name'],
                                                           last_name=user_details_form.cleaned_data['last_name'],
                                                           email=user_details_form.cleaned_data['email'],
                                                           password=user_details_form.cleaned_data['password'],
                                                           organization=user_details_form.cleaned_data['organization'],
                                                           mobile_number=user_details_form.cleaned_data['mobile_number'],
                                                           role=user_details_form.cleaned_data['role']
                                                           )
            registered = True
        else:
            print 'Error in User Details Form'
            print user_details_form.errors
    else:
        context_dic['user_details_form'] = UserDetailsForm()

    context_dic['registered'] = registered
    return render(request,'authentication/register.html', context_dic)


def login(request):
    context_dic ={}
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage', args=(request)))
    else:
        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            # print username, password
            user = authenticate(username = username, password = password)

            if user:
                print "authenticate successfull"
                auth_login(request, user)
                return HttpResponseRedirect( reverse('homepage'))
            else:
                return HttpResponse('Invalid Login Details')

    return render(request, 'authentication/login.html', context_dic)


@login_required
def homePage(request):
    return render(request, 'Home.html')


@login_required
def getPartailtemplate(request):
    return render(request, 'scheduleManagement/_timeline_modal.html')


def request_quote(request):
    posted_data = string_to_dict(request.body)
    success = False
    errors = []
    if request.method == 'POST':
        request_quote_form = RequestQuoteForm(data=posted_data)
        if request_quote_form.is_valid():
            try:
                request_quote_form.save()
            except:
                error = "Error while saving the requested Quote"
                errors.append(error)
                print error
        else:
            error = "Request Quote form data is not valid"
            errors.append(error)
            print error
    return ajax_response(success=success, errors=errors)


# def logout(request):
#     print 'I am in logout'
#     auth_logout(request)
#     return HttpResponse('User logged out successfully.')

#private methods

'''
def setSessionVar(request, status):
    request.session['userLoggedIn'] = status
'''


