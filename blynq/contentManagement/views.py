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
from customLibrary.views_lib import ajax_response, user_and_organization, string_to_dict
from customLibrary.serializers import FlatJsonSerializer as json_serializer
from contentManagement.models import Content


@login_required
def index(request):
    # context_dic = {}
    # context_dic['form'] = UploadContentForm(form_name='formUpload', scope_prefix='mdlNewFileDetailsObj')
    # print context_dic
    return render(request,'contentManagement/content_index.html')


@login_required
def upload_content(request):
    errors = []
    success = False
    user_details, organization = user_and_organization(request)
    try:
        import pdb;pdb.set_trace()
        document = request.FILES['file']
        # posted_data = string_to_dict(request.body)
        title = 'hello' #posted_data.get('title')
        parent_folder_id = -1 # posted_data.get('currentFolderId')
        if parent_folder_id == -1:
            parent_folder = None
        else:
            parent_folder = Content.objects.get(content_id=parent_folder_id)
        Content.objects.create(title=title,
                               document=document,
                               uploaded_by=user_details,
                               last_modified_by=user_details,
                               organization=organization,
                               parent_folder=parent_folder,
                               is_folder=False)
        success = True
    except:
        error = 'Error while uploading the file'
        print error
        errors.append(error)
    return ajax_response(success=success, errors=errors)


def delete_folder_helper(req_content, user_content):
    user_content = user_content.filter(parent_folder__pk=req_content.content_id)
    for content in user_content:
        if content.is_folder:
            delete_folder_helper(req_content=content, user_content=user_content)
        else:
            delete_file_helper(content)
    req_content.delete()


def delete_file_helper(content):
    os.remove(BASE_DIR+content.document.url)
    content.delete()


@login_required
def delete_content(request, content_id):
    user_details, organization = user_and_organization(request)
    user_content = Content.objects.filter(Q(uploaded_by=user_details) | Q(organization=organization))
    try:
        required_content = user_content.get(content_id=int(content_id))
        if required_content.is_folder:
            delete_folder_helper(req_content=required_content, user_content=user_content)
        else:
            delete_file_helper(required_content)
        success=True
    except:
        success=False
    return ajax_response(success=success)


@login_required
def create_folder(request):
    #data in request.body- components passes "currentFolderId", "title"
    errors = []
    success = False
    user_details, organization = user_and_organization(request)
    try:
        posted_data = string_to_dict(request.body)
        parent_folder_id = posted_data.get('currentFolderId')
        if parent_folder_id == -1:
            parent_folder = None
        else:
            parent_folder = Content.objects.get(content_id=parent_folder_id)
        title = posted_data.get('title')
        Content.objects.create(title=title,
                               document=None,
                               uploaded_by=user_details,
                               last_modified_by=user_details,
                               organization=organization,
                               parent_folder=parent_folder,
                               is_folder=True)
        success = True
    except:
        error = 'Error with the submitted data in create folder'
        print error
        errors.append(error)
    return ajax_response(success=success, errors=errors)


def get_tree_view(request, folder_id=-1):
    folder_id = int(folder_id)
    tree_view = []
    json_folders = get_folders_json(request, folder_id)
    for folder in json_folders:
        folder['folders'] = get_tree_view(request, folder.get('content_id'))
    tree_view = json_folders
    return tree_view


def get_content_helper(request, parent_folder_id=-1, is_folder=False):
    user_details, organization = user_and_organization(request)
    user_content = Content.objects.filter(Q(uploaded_by=user_details) | Q(organization=organization)).filter(is_folder=is_folder)
    parent_folder_id = int(parent_folder_id)
    if parent_folder_id == -1:
        user_content = user_content.filter(parent_folder=None)
    else:
        parent_folder = Content.objects.get(parent_folder_id)
        user_content = user_content.filter(parent_folder=parent_folder)
    json_content = json_serializer().serialize(user_content, fields=('title', 'description', 'document', 'content_id'))
    return HttpResponse(json_content, content_type='application/json')


def get_folders_json(request, parent_folder_id=-1):
    return get_content_helper(request, parent_folder_id=parent_folder_id, is_folder=True)


def get_files_json(request, parent_folder_id=-1):
    return get_content_helper(request, parent_folder_id=parent_folder_id, is_folder=False)
