import json

from django.core import serializers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from JsonTestData import TestDataClass
from django.http import JsonResponse, HttpResponse
from authentication.models import UserDetails
from contentManagement.forms import UploadContentForm
# Create your views here.
from screenManagement.views import user_and_organization
from screenManagement.serializers import FlatJsonSerializer as json_serializer
from contentManagement.models import Content
from django.db.models import Q


@login_required
def index(request):
    context_dic = {}
    context_dic['form'] = UploadContentForm(form_name='formUpload', scope_prefix='mdlNewFileObj')
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
            user_details, organization = user_and_organization(request)
            form_data = upload_content_form.cleaned_data
            Content.objects.create(title=form_data.get('title'),
                                   description=form_data.get('description'),
                                   document=form_data.get('document'),
                                   uploaded_by=user_details,
                                   last_modified_by=user_details,
                                   organization=organization,
                                   parent_folder=None)
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


def get_user_content(request, folder_id=-1):
    user_details, organization = user_and_organization(request)
    user_content = Content.objects.filter(Q(uploaded_by=user_details) | Q(organization=organization))
    if folder_id == -1:
        user_content = user_content.filter(parent_folder__isnull=True)
    else:
        user_content = user_content.filter(parent_folder__pk=folder_id)
    folders = user_content.filter(is_folder=True)
    files = user_content.filter(is_folder=False)
    json_folders_data = json_serializer().serialize(folders,
                                            fields=('title', 'description', 'document'))
    json_files_data = json_serializer().serialize(files,
                                            fields=('title', 'description', 'document'))
    json_data = {'folders' : json_folders_data, 'files' : json_files_data}
    #json_data = json.dumps(json_data)
    #print json_data
    return JsonResponse(json_data, safe=False)

def get_folders_json(request, folder_id=-1):
    user_details, organization = user_and_organization(request)
    folders_content = Content.objects.filter(Q(uploaded_by=user_details) | Q(organization=organization))
    if folder_id == -1:
        folders_content = folders_content.filter(parent_folder__isnull=True)
    else:
        folders_content = folders_content.filter(parent_folder__pk=folder_id)
    json_folders = json_serializer().serialize(folders_content, fields=('title', 'description', 'document'))
    return HttpResponse(json_folders, content_type='application/json')

def get_files_json(request, folder_id=-1):
    user_details, organization = user_and_organization(request)
    files_content = Content.objects.filter(Q(uploaded_by=user_details) | Q(organization=organization))
    if folder_id == -1:
        files_content = files_content.filter(parent_folder__isnull=True)
    else:
        files_content = files_content.filter(parent_folder__pk=folder_id)
    json_files = json_serializer().serialize(files_content, fields=('title', 'description', 'document'))
    return HttpResponse(json_files, content_type='application/json')
