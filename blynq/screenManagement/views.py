from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from JsonTestData import TestDataClass
from django.http import JsonResponse

#from models import
# Create your views here.

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

