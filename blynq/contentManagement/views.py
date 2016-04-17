from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from JsonTestData import TestDataClass
from django.http import JsonResponse

from authentication.models import UserDetails
from contentManagement.forms import UploadContentForm
# Create your views here.
from contentManagement.models import Content


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


@login_required
def upload_content(request):
    context_dic = {}
    success = False
    if request.method == 'POST':
        upload_content_form = UploadContentForm(request.POST, request.FILES)
        if upload_content_form.is_valid():
            user_details = UserDetails.objects.get(username=request.user.username)
            form_data = upload_content_form.cleaned_data
            Content.objects.create(title=form_data.get('title'),
                                   description=form_data.get('description'),
                                   document=form_data.get('document'),
                                   uploaded_by=user_details,
                                   last_modified_by=user_details)
            success = True
            success_message = "The Screen has been successfully Added."
            context_dic['success_message'] = success_message
        else:
            print 'Upload Content Form is not valid'
            print upload_content_form.errors
    else:
        context_dic['form'] = UploadContentForm()
        # TODO: Not able to unselect the Group field once selected, fix this issue in the frontend.
    context_dic['title'] = "Upload File"
    context_dic['submitButton'] = "Submit"
    context_dic['success'] = success
    context_dic['target'] = reverse('upload_content')
    return render(request,'Shared/displayForm.html', context_dic)
