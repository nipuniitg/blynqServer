import mimetypes
import os
import subprocess
from copy import deepcopy

from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.db import transaction
from django.shortcuts import render

from contentManagement.serializers import ContentSerializer
from customLibrary.views_lib import ajax_response, get_userdetails, string_to_dict, obj_to_json_response, \
    debugFileLog, full_file_path
from contentManagement.models import Content, ContentType


# Create your views here.


@login_required
def index(request):
    # context_dic = {}
    # context_dic['form'] = UploadContentForm(form_name='formUpload', scope_prefix='mdlNewFileDetailsObj')
    # print context_dic
    return render(request, 'contentManagement/content_index.html')


@login_required
def upsert_url(request):
    errors = []
    success = False
    try:
        user_details = get_userdetails(request)
        posted_data = string_to_dict(request.body)
        parent_folder_id = int(posted_data.get('parent_folder_id'))
        if parent_folder_id == -1:
            parent_folder = None
        else:
            parent_folder = Content.get_user_relevant_objects(user_details=user_details).get(
                content_id=parent_folder_id)
        posted_content = posted_data.get('content')
        content_id = int(posted_content.get('content_id'))
        content_id = None if content_id == -1 else content_id
        title = posted_content.get('title')
        url = posted_content.get('url')
        if url:
            content_dict = dict(title=title, url=url, uploaded_by=user_details, parent_folder=parent_folder,
                                last_modified_by=user_details, organization=user_details.organization)
            instance, created = Content.get_user_relevant_objects(user_details=user_details).get_or_create(
                content_id=content_id, defaults=content_dict)
            if not created:
                for attr, value in content_dict.iteritems():
                    setattr(instance, attr, value)
                instance.save()
            success = True
        else:
            errors = ['Please enter a valid URL']
    except Exception as e:
        debugFileLog.exception('Received exception')
        debugFileLog.exception(e)
        errors = str(e)
    return ajax_response(success=success, errors=errors)


def process_media(file_path, parent_folder=None, user_details=None, organization=None):
    debugFileLog.info('Inside process_media')
    if not file_path or not os.path.exists(file_path):
        debugFileLog.info('File path does not exist')
        return True
    file_type, encoding = mimetypes.guess_type(str(file_path))
    if 'image' in file_type:
        return compress_image(file_path, parent_folder, user_details, organization)
    elif 'video' in file_type:
        return compress_video(file_path, parent_folder, user_details, organization)
    else:
        return True


def compress_image(file_path, parent_folder=None, user_details=None, organization=None):
    img = Image.open(file_path)
    img = img.resize(img.size, Image.ANTIALIAS)
    filename = os.path.basename(file_path)
    title, ext = os.path.splitext(filename)
    dest_filepath = filename
    img.save(dest_filepath, optimize=True, quality=95)
    img_file = open(dest_filepath)
    django_file = File(img_file)
    content = Content(title=title, document=django_file, uploaded_by=user_details, last_modified_by=user_details,
                      organization=user_details.organization, parent_folder=parent_folder, is_folder=False)
    content.save()
    try:
        os.remove(filename)
    except Exception as e:
        debugFileLog.exception('Not able to delete compressed temp file')
        debugFileLog.exception(e)
    return True


def compress_video(file_path, parent_folder=None, user_details=None, organization=None):
    filename = os.path.basename(file_path)
    title, ext = os.path.splitext(filename)
    temp_file_path = full_file_path(relative_path='temp/converted_' + title + '.mp4')
    try:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        # resolution_width = 480
        # cmd = "eval $(ffprobe -v error -of flat=s=_ -select_streams v:0 -show_entries stream=height,width %s);" \
        #       " echo ${streams_stream_0_width}" % file_path
        # output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        # for line in output.stdout:
        #     if re.match('[0-9]+$', line):
        #         resolution_width = int(line)
        convert_cmd = 'ffmpeg -i "%s" -vcodec libx264 -vprofile high -preset medium -vf ' \
                      '"scale=2*trunc(iw/2):-2" -threads  0 -acodec copy -b:a 128k "%s"' % (file_path, temp_file_path)
        p = subprocess.Popen(convert_cmd, shell=True, stdout=subprocess.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            debugFileLog.exception("Video conversion failed with error %d %s %s" % (p.returncode, output, error))
            return False
        video_file = open(temp_file_path)
        django_file = File(video_file)
        content = Content(title=title, document=django_file, uploaded_by=user_details, last_modified_by=user_details,
                          organization=organization, parent_folder=parent_folder)
        content.save()
        try:
            os.remove(temp_file_path)
        except Exception as e:
            debugFileLog.exception('Not able to remove the temp file while video conversion %s' % temp_file_path)
            debugFileLog.exception(e)
        return True
    except Exception as e:
        debugFileLog.exception(e)
        return False


@login_required
def upload_content(request):
    errors = []
    success = True
    conversion_success = True
    try:
        user_details = get_userdetails(request)
        posted_data = request.POST
        total_files = int(posted_data.get('totalFiles'))
        parent_folder_id = int(posted_data.get('currentFolderId'))
        if total_files <= 0:
            error_str = 'Error in the total files received'
            debugFileLog.error(error_str)
            return ajax_response(success=success, errors=errors)
        for i in range(total_files):
            key = 'file' + str(i)
            document = request.FILES[key]
            title = os.path.splitext(document.name)[0]
            try:
                if parent_folder_id == -1:
                    parent_folder = None
                else:
                    parent_folder = Content.get_user_relevant_objects(user_details).get(content_id=parent_folder_id)
                    assert parent_folder.is_folder
                content = Content(title=title, document=document, uploaded_by=user_details,
                                  last_modified_by=user_details, organization=user_details.organization,
                                  parent_folder=parent_folder, is_folder=False)
                content.save()
                if content.is_image or content.is_video:
                    file_path = full_file_path(relative_path=content.document.name)
                    if not process_media(file_path, parent_folder=parent_folder, user_details=user_details,
                                         organization=user_details.organization):
                        error_str = 'Error while processing media file %s' % document.name
                        errors.append(error_str)
                        debugFileLog.exception(error_str)
                        conversion_success = False
                    content.delete()
            except AssertionError:
                success = False
                error_str = "Improper parent folder, please refresh the page and try again"
                debugFileLog.exception(error_str)
                errors.append(error_str)
            except Exception as e:
                success = False
                error_str = 'Error while uploading the file %s ' % document.name
                debugFileLog.exception(error_str)
                errors.append(error_str)
        success = success and conversion_success
    except Exception as e:
        success = False
        error_str = 'Error while uploading the file'
        debugFileLog.exception(error_str)
        errors.append(error_str)
    return ajax_response(success=success, errors=errors)


@transaction.atomic
@login_required
def delete_content(request):
    user_details = get_userdetails(request)
    # user_content = Content.objects.filter(Q(uploaded_by=user_details) | Q(organization=organization))
    user_content = Content.get_user_relevant_objects(user_details=user_details)
    posted_data = string_to_dict(request.body)
    content_ids = posted_data.get('content_ids')
    deleted_content_ids = []
    sid = -1
    try:
        with transaction.atomic():
            for content_id in content_ids:
                required_content = user_content.get(content_id=int(content_id))
                required_content.delete()
                sid = transaction.savepoint()
                deleted_content_ids.append(content_id)
            success = True
    except Exception as e:
        debugFileLog.error('Exception is')
        debugFileLog.error(e)
        success = False
        if sid != -1:
            transaction.savepoint_rollback(sid)
    return ajax_response(success=success, errors='Invalid content',
                         obj_dict={'deleted_content_ids': deleted_content_ids})


@login_required
def create_folder(request):
    # data in request.body- components passes "currentFolderId", "title"
    errors = []
    success = False
    user_details = get_userdetails(request)
    try:
        posted_data = string_to_dict(request.body)
        parent_folder_id = int(posted_data.get('currentFolderId'))
        if parent_folder_id == -1:
            parent_folder = None
        else:
            parent_folder = Content.get_user_relevant_objects(user_details=user_details).get(
                content_id=parent_folder_id)
        title = posted_data.get('title')
        Content.objects.create(title=title,
                               document=None,
                               uploaded_by=user_details,
                               last_modified_by=user_details,
                               organization=user_details.organization,
                               parent_folder=parent_folder,
                               is_folder=True)
        success = True
    except Exception as e:
        debugFileLog.exception(e)
        errors = 'Error with the submitted data in create folder'
    return ajax_response(success=success, errors=errors)


# def get_tree_view(request, parent_folder_id=-1):
#     parent_folder_id = int(parent_folder_id)
#     tree_view = []
#     json_folders = get_folders_json(request, parent_folder_id)
#     for folder in json_folders:
#         folder['folders'] = get_tree_view(request, folder.get('content_id'))
#     tree_view = json_folders
#     return tree_view


def get_files_recursively(request, parent_folder_id=-1):
    user_details = get_userdetails(request)
    user_content = Content.get_user_relevant_objects(user_details=user_details)
    parent_folder_id = int(parent_folder_id)
    if parent_folder_id == -1:
        parent_folder = None
    else:
        parent_folder = user_content.get(content_id=parent_folder_id)
    all_files_content_id = []
    current_folder_files = user_content.filter(parent_folder=parent_folder, is_folder=False)
    for each_file in current_folder_files:
        all_files_content_id.append(each_file.content_id)

    current_folder_folders = user_content.filter(parent_folder=parent_folder, is_folder=True)
    for folder in current_folder_folders:
        current_folder_files = get_files_recursively(request, parent_folder_id=folder.content_id)
        all_files_content_id = all_files_content_id + current_folder_files

    return all_files_content_id


def folder_path(request, current_folder_id):
    current_folder_id = int(current_folder_id)
    user_details = get_userdetails(request)
    path = []
    if current_folder_id != -1:
        user_content = Content.get_user_relevant_objects(user_details=user_details).get(content_id=current_folder_id)
        path = user_content.logical_path_list()
    home_folder = {'content_id': -1, 'title': 'Home'}
    path.insert(0, home_folder)
    return obj_to_json_response(path)


def get_valid_content_types(request):
    unicode_content_types = ContentType.objects.all().values_list('file_type', flat=True)
    str_content_types = [str(content_type) for content_type in unicode_content_types]
    return obj_to_json_response(str_content_types)


def get_content_helper(request, parent_folder_id=-1, is_folder=False):
    try:
        user_details = get_userdetails(request)
        # Below line is to get content for both user and organization
        # user_content = Content.objects.filter(Q(uploaded_by=user_details) | Q(organization=organization))
        user_content = Content.get_user_relevant_objects(user_details=user_details)
        parent_folder_id = int(parent_folder_id)
        if parent_folder_id == -1:
            user_content = user_content.filter(parent_folder=None)
        else:
            parent_folder = user_content.get(content_id=parent_folder_id)
            user_content = user_content.filter(parent_folder=parent_folder)
        user_content = user_content.filter(is_folder=is_folder)
        json_data = ContentSerializer().serialize(user_content,
                                                  fields=('title', 'document', 'content_type', 'content_id',
                                                          'is_folder'), use_natural_foreign_keys=True)
    except Exception as e:
        debugFileLog.exception(e)
        json_data = []
        debugFileLog.exception("Error while fetching the content or invalid parent folder id")
    return obj_to_json_response(json_data)


def get_folders_json(request, parent_folder_id=-1):
    """
    :param request:
    :param parent_folder_id:
    :return:
    [
        {
            url: "",
            content_id: 2,
            is_folder: true,
            title: "temp folder",
            content_type: None
        }
    ]
    """

    return get_content_helper(request, parent_folder_id=parent_folder_id, is_folder=True)


def get_files_json(request, parent_folder_id=-1):
    """
    :param request:
    :param parent_folder_id:
    :return:
    [
        {
            url: "http://127.0.0.1:8000/media/usercontent/1/image1.jpg",
            content_id: 1,
            is_folder: false,
            title: "image1",
            content_type: "image/jpeg"
        }
    ]
    """

    return get_content_helper(request, parent_folder_id=parent_folder_id, is_folder=False)


def update_content_title(request):
    user_details = get_userdetails(request)
    success = False
    errors = []
    posted_data = string_to_dict(request.body)
    title = posted_data.get('title')
    content_id = posted_data.get('content_id')
    content_id = int(content_id)
    if content_id != -1:
        try:
            content = Content.get_user_relevant_objects(user_details=user_details).get(content_id=content_id)
            content.title = title
            content.save()
            success = True
        except Exception as e:
            debugFileLog.exception(e)
            error = 'Error while saving the title to the database'
            errors.append(error)
    return ajax_response(success=success, errors=errors)


@login_required
def move_content(request):
    user_details = get_userdetails(request)
    success = True
    errors = []
    posted_data = string_to_dict(request.body)
    content_ids = posted_data.get('content_ids')
    parent_folder_id = int(posted_data.get('parent_folder_id'))
    debugFileLog.info( 'parent_folder_id is %d' % parent_folder_id )
    user_content = Content.get_user_relevant_objects(user_details=user_details)
    try:
        if parent_folder_id == -1:
            parent_folder = None
        else:
            parent_folder = user_content.get(content_id=parent_folder_id)
        # assert parent_folder.is_folder == True
    except Content.DoesNotExist:
        success = False
        error = 'You dont have permission to move the selected content. ' \
                'Please refresh and try again if you think, you should have permission'
        return ajax_response(success=success, errors=errors)
    for content_id in content_ids:
        try:
            content = user_content.get(content_id=content_id)
            content.parent_folder = parent_folder
            content.save()
        except Content.DoesNotExist:
            success = False
            error = 'Error occured while moving the items. please refresh and try again.'
    return ajax_response(success=success, errors=errors)
