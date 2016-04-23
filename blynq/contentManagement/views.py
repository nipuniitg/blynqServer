import os
import shutil

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q

from blynq.settings import BASE_DIR
from contentManagement.forms import UploadContentForm
# Create your views here.
from customLibrary.views_lib import ajax_response, user_and_organization
from customLibrary.serializers import FlatJsonSerializer as json_serializer
from contentManagement.models import Content


@login_required
def index(request):
    context_dic = {}
    context_dic['form'] = UploadContentForm(form_name='formUpload', scope_prefix='mdlNewFileDetailsObj')
    print context_dic
    return render(request,'contentManagement/content_index.html', context_dic)


@login_required
def upload_content(request):
    context_dic = {}
    success = False
    import pdb; pdb.set_trace()
    print request.FILES
    if request.method == 'POST':
        upload_content_form = UploadContentForm(request.POST, request.FILES)
        if upload_content_form.is_valid():
            user_details, organization = user_and_organization(request)
            form_data = upload_content_form.cleaned_data
            Content.objects.create(title=form_data.get('title'),
                                   document=form_data.get('document'),
                                   uploaded_by=user_details,
                                   last_modified_by=user_details,
                                   organization=organization,
                                   parent_folder=None)
            success = True
            success_message = "File upload successful."
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


# Helper function
def delete_folder(req_content, user_content):
    user_content = user_content.filter(parent_folder__pk=req_content.content_id)
    for content in user_content:
        if content.is_folder:
            delete_folder(req_content=content, user_content=user_content)
        else:
            delete_file(content)
    req_content.delete()


# Helper function
def delete_file(content):
    os.remove(BASE_DIR+content.document.url)
    content.delete()


@login_required
def delete_content(request, content_id):
    user_details, organization = user_and_organization(request)
    user_content = Content.objects.filter(Q(uploaded_by=user_details) | Q(organization=organization))
    try:
        required_content = user_content.get(content_id=content_id)
        if required_content.is_folder:
            delete_folder(req_content=required_content, user_content=user_content)
        else:
            delete_file(required_content)
        success=True
    except:
        success=False
    return ajax_response(success=success)


def get_tree_view(request, folder_id=-1):
    tree_view = []
    json_folders = get_folders_json(request, folder_id)
    for folder in json_folders:
        folder['folders'] = get_tree_view(request, folder.get('content_id'))
    tree_view = json_folders
    return tree_view


def get_folders_json(request, folder_id=-1):
    user_details, organization = user_and_organization(request)
    folders_content = Content.objects.filter(Q(uploaded_by=user_details) | Q(organization=organization))
    if folder_id == -1:
        folders_content = folders_content.filter(parent_folder__isnull=True)
    else:
        folders_content = folders_content.filter(parent_folder__pk=folder_id)
    json_folders = json_serializer().serialize(folders_content, fields=('title', 'description', 'document', 'content_id'))
    return HttpResponse(json_folders, content_type='application/json')


def get_files_json(request, folder_id=-1):
    user_details, organization = user_and_organization(request)
    files_content = Content.objects.filter(Q(uploaded_by=user_details) | Q(organization=organization))
    if folder_id == -1:
        files_content = files_content.filter(parent_folder__isnull=True)
    else:
        files_content = files_content.filter(parent_folder__pk=folder_id)
    json_files = json_serializer().serialize(files_content, fields=('title', 'description', 'document', 'content_id'))
    return HttpResponse(json_files, content_type='application/json')
