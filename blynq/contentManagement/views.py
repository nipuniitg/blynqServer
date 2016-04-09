from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from JsonTestData import TestDataClass
from django.http import JsonResponse
# Create your views here.

@login_required
def index(request):
    return render(request,'contentManagement/content_index.html')


@login_required
def getContentJson(request):
    classObj = TestDataClass()
    content = classObj.getContentTestData()
    return JsonResponse(content, safe=False)


def deleteItem(request):
    print request
    itemId= request.itemId
    actionStatus = {'actionStatus' : 'success'}
    return JsonResponse(actionStatus, safe=False)


@login_required
def deleteFolder(request):
    folderId= request.folderId
    actionStatus = {'actionStatus' : 'success'}
    return JsonResponse(actionStatus, safe=False)
