import mimetypes
import os
import subprocess
import urllib2
import json
import StringIO
import zipfile

from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

from PIL import Image

from contentManagement.serializers import default_content_serializer
from blynq.settings import TEMP_DIR, MEDIA_ROOT, USERCONTENT_DIR
from customLibrary.custom_settings import COMPRESS_IMAGE, WIDGET_SCROLL_TIME
from customLibrary.views_lib import ajax_response, get_userdetails, string_to_dict, obj_to_json_response, \
    debugFileLog, full_file_path, mail_exception, timeit, empty_string_for_none
from contentManagement.models import Content, ContentType, FbWidget


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
            parent_folder = Content.get_user_filesystem(user_details=user_details).get(
                content_id=parent_folder_id)
        posted_content = posted_data.get('content')
        content_id = int(posted_content.get('content_id'))
        content_id = None if content_id == -1 else content_id
        title = posted_content.get('title')
        url = posted_content.get('url')
        if url:
            content_dict = dict(title=title, url=url, uploaded_by=user_details, parent_folder=parent_folder,
                                last_updated_by=user_details, organization=user_details.organization)
            instance, created = Content.get_user_filesystem(user_details=user_details).get_or_create(
                content_id=content_id, defaults=content_dict)
            if not created:
                for attr, value in content_dict.iteritems():
                    setattr(instance, attr, value)
                instance.save()
            success = True
        else:
            errors = ['Please enter a valid URL']
    except Exception as e:
        debugFileLog.error('Request body is %s' % request.body)
        mail_exception(exception=e)
        errors = 'Error while creating the new URL, a mail has already been sent to the support team.'
    return ajax_response(success=success, errors=errors)


def process_media(file_path, parent_folder=None, user_details=None, organization=None, content_already_saved=True):
    debugFileLog.info('Inside process_media')
    if not file_path or not os.path.exists(file_path):
        debugFileLog.info('File path does not exist')
        return False, False
    file_type, encoding = mimetypes.guess_type(str(file_path))
    if 'image' in file_type:
        return compress_image(file_path, parent_folder, user_details, organization, content_already_saved)
    elif 'video' in file_type:
        return compress_video(file_path, parent_folder, user_details, organization, content_already_saved)
    else:
        return True, False


def compress_image(file_path, parent_folder=None, user_details=None, organization=None, content_already_saved=False):
    try:
        filename = os.path.basename(file_path)
        title, ext = os.path.splitext(filename)
        if COMPRESS_IMAGE:
            img = Image.open(file_path)
            img = img.resize(img.size, Image.ANTIALIAS)
            dest_filepath = os.path.join(TEMP_DIR, filename)
            img.save(dest_filepath, optimize=True, quality=95)
            img_file = open(dest_filepath)
        else:
            img_file = open(file_path)
        django_file = File(img_file)
        if content_already_saved:
            if COMPRESS_IMAGE:
                content = Content(title=title, document=django_file, uploaded_by=user_details, last_updated_by=user_details,
                                  organization=user_details.organization, parent_folder=parent_folder, is_folder=False)
                content.save()
            else:
                return False, False
        else:
            content = Content(title=title, document=django_file, uploaded_by=user_details, last_updated_by=user_details,
                              organization=user_details.organization, parent_folder=parent_folder, is_folder=False)
            content.save()

        # if COMPRESS_IMAGE:
        #     try:
        #         os.remove(filename)
        #     except Exception as e:
        #         debugFileLog.exception('Not able to delete compressed temp file')
        #         mail_exception(exception=e)
        conversion_successful = True
        delete_old = True
    except Exception as e:
        debugFileLog.error('compress_image inputs are ' + 'file_path ' + str(file_path) + ' parent_folder ' +
                           str(parent_folder) + ' user_details ' + str(user_details) +
                           ' organization ' + str(organization) + 'content_already_saved ' + str(content_already_saved))
        mail_exception(exception=e)
        conversion_successful = False
        delete_old = False
    return conversion_successful, delete_old


def video_conversion_required(file_path):
    return True
    # try:
    #     cmd = "ffprobe -show_format -show_streams -loglevel quiet -print_format json '%s'" % file_path
    #     subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)


@timeit
def compress_video(file_path, parent_folder=None, user_details=None, organization=None, content_already_saved=False):
    delete_old = True
    conversion_successful = False
    try:
        filename = os.path.basename(file_path)
        title, ext = os.path.splitext(filename)
        temp_file_path = full_file_path(relative_path='temp/converted_' + title + '.mp4')
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        # resolution_width = 480
        # cmd = "eval $(ffprobe -v error -of flat=s=_ -select_streams v:0 -show_entries stream=height,width %s);" \
        #       " echo ${streams_stream_0_width}" % file_path
        # output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        # for line in output.stdout:
        #     if re.match('[0-9]+$', line):
        #         resolution_width = int(line)
        convert_cmd = 'ffmpeg -i "%s" -movflags faststart -vcodec libx264 -vprofile baseline -preset medium -vf ' \
                      '"scale=2*trunc(iw/2):-2" -threads  0 -acodec copy -strict -2 -b:a 128k "%s"' % (file_path, temp_file_path)
        p = subprocess.Popen(convert_cmd, shell=True, stdout=subprocess.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            debugFileLog.exception("Video conversion failed with error %d %s %s" % (p.returncode, output, error))
            return conversion_successful, delete_old
        video_file = open(temp_file_path)
        django_file = File(video_file)
        content = Content(title=title, document=django_file, uploaded_by=user_details, last_updated_by=user_details,
                          organization=organization, parent_folder=parent_folder)
        content.save()
        conversion_successful = True
        try:
            os.remove(temp_file_path)
        except Exception as e:
            debugFileLog.exception('Not able to remove the temp file while video conversion %s' % temp_file_path)
            mail_exception(exception=e)
        return conversion_successful, delete_old
    except Exception as e:
        debugFileLog.error('compress_image inputs are ' + 'file_path ' + str(file_path) + ' parent_folder ' +
                           str(parent_folder) + ' user_details ' + str(user_details) +
                           ' organization ' + str(organization) + 'content_already_saved ' + str(content_already_saved))
        mail_exception(exception=e)
        return conversion_successful, delete_old


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
            return ajax_response(success=success, errors=[error_str])
        for i in range(total_files):
            if user_details.organization.usage_exceeded():
                return ajax_response(success=False, errors=[
                    "You already exceeded your usage limits, please contact support@blynq.in to upgrade your plan"])
            key = 'file' + str(i)
            document = request.FILES[key]
            title = os.path.splitext(document.name)[0]
            try:
                if parent_folder_id == -1:
                    parent_folder = None
                else:
                    parent_folder = Content.get_user_filesystem(user_details).get(content_id=parent_folder_id)
                    assert parent_folder.is_folder
                content = Content.objects.create(title=title, document=document, uploaded_by=user_details,
                                                 last_updated_by=user_details, organization=user_details.organization,
                                                 parent_folder=parent_folder, is_folder=False)
                # Saving the content twice so that the duration can be found out using content.document
                content.save()
                if content.is_image or content.is_video:
                    file_path = full_file_path(relative_path=content.document.name)
                    media_compressed, delete_old = process_media(
                        file_path, parent_folder=parent_folder, user_details=user_details,
                        organization=user_details.organization, content_already_saved=True)
                    if not media_compressed:
                        error_str = 'Error while processing media file %s' % document.name
                        errors.append(error_str)
                        debugFileLog.exception(error_str)
                        if delete_old:
                            conversion_success = False
                        else:
                            conversion_success = True
                    if delete_old:
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
        debugFileLog.error('Request post is ' + str(request.POST))
        error_str = 'Error while uploading the file'
        debugFileLog.error(e)
        errors.append(error_str)
    return ajax_response(success=success, errors=errors)


@transaction.atomic
@login_required
def delete_content(request):
    success = False
    deleted_content_ids = []
    user_details = get_userdetails(request)
    # user_content = Content.objects.filter(Q(uploaded_by=user_details) | Q(organization=organization))
    try:
        user_content = Content.get_user_filesystem(user_details=user_details)
        posted_data = string_to_dict(request.body)
        content_ids = posted_data.get('content_ids')
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
    except Exception as e:
        debugFileLog.error('request body is ' + str(request.body))
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
            parent_folder = Content.get_user_filesystem(user_details=user_details).get(
                content_id=parent_folder_id)
        title = posted_data.get('title')
        Content.objects.create(title=title,
                               document=None,
                               uploaded_by=user_details,
                               last_updated_by=user_details,
                               organization=user_details.organization,
                               parent_folder=parent_folder,
                               is_folder=True)
        success = True
    except Exception as e:
        debugFileLog.error('request body is ' + str(request.body))
        mail_exception(exception=e)
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
    user_content = Content.get_user_filesystem(user_details=user_details)
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
        user_content = Content.get_user_filesystem(user_details=user_details).get(content_id=current_folder_id)
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
        user_content = Content.get_user_filesystem(user_details=user_details)
        parent_folder_id = int(parent_folder_id)
        if parent_folder_id == -1:
            user_content = user_content.filter(parent_folder=None)
        else:
            parent_folder = user_content.get(content_id=parent_folder_id)
            user_content = user_content.filter(parent_folder=parent_folder)
        user_content = user_content.filter(is_folder=is_folder)
        json_data = default_content_serializer(user_content)
    except Exception as e:
        mail_exception(exception=e)
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
            content = Content.get_user_filesystem(user_details=user_details).get(content_id=content_id)
            content.title = title
            content.save()
            success = True
        except Exception as e:
            debugFileLog.error('request body is ' + str(request.body))
            mail_exception(exception=e)
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
    user_content = Content.get_user_filesystem(user_details=user_details)
    try:
        if parent_folder_id == -1:
            parent_folder = None
        else:
            parent_folder = user_content.get(content_id=parent_folder_id)
        # assert parent_folder.is_folder == True
    except Content.DoesNotExist:
        success = False
        error = 'You do not have permission to move the selected content. ' \
                'Please refresh and try again if you think, you should have permission'
        return ajax_response(success=success, errors=errors)
    for content_id in content_ids:
        try:
            content = user_content.get(content_id=content_id)
            content.parent_folder = parent_folder
            content.save()
        except Content.DoesNotExist:
            success = False
            error = 'Error occurred while moving the items. please refresh and try again.'
    return ajax_response(success=success, errors=errors)


@login_required
def create_and_download_zip(request):
    user_details = get_userdetails(request)
    try:
        user_folder = "user%d" % user_details.user.id
        usercontent_dir = os.path.join(MEDIA_ROOT, USERCONTENT_DIR)
        user_directory = os.path.join(usercontent_dir, user_folder)
        zip_subdir = user_details.user.username
        zip_filename = "%s.zip" % zip_subdir
        # zip_fullname = os.path.join(usercontent_dir, zip_filename)

        # Open StringIO to grab in-memory ZIP contents
        s = StringIO.StringIO()

        # The zip compressor
        zf = zipfile.ZipFile(s, "w")

        for fname in os.listdir(user_directory):
            # Calculate path for file in zip
            zip_path = os.path.join(zip_subdir, fname)

            fpath = os.path.join(user_directory, fname)
            # Add file, at correct path
            zf.write(fpath, zip_path)

        zf.close()
        # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(s.getvalue(), content_type="application/zip")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
        return resp
    except Exception as e:
        debugFileLog.exception(str(e))
        return ajax_response(success=False,
                             errors=["There is some error while creating a zip to download. Please contact support"])


def get_widgets(request):
    user_details = get_userdetails(request)
    widgets = Content.get_user_widgets(user_details=user_details)
    json_data = default_content_serializer(widgets)
    return obj_to_json_response(json_data)


def delete_widget(request):
    debugFileLog.info('Inside delete widget')
    success = False
    errors = []
    try:
        user_details = get_userdetails(request)
        posted_data = string_to_dict(request.body)
        content_id = int(posted_data.get('content_id'))
        widget = Content.get_user_widgets(user_details=user_details).get(content_id=content_id)
        widget.delete()
        success = True
    except Exception as e:
        errors = ['Access denied to delete this widget']
        mail_exception(exception=e)
    return ajax_response(success=success, errors=errors)


def upsert_widget(request):
    debugFileLog.info("Inside upsert widget")
    success = False
    errors = []
    try:
        user_details = get_userdetails(request)
        posted_data = string_to_dict(request.body)
        content_id = int(posted_data.get('content_id'))
        title = posted_data.get('title')
        # TODO: Remove this hard-coding of widget/rss/text
        content_type, created = ContentType.objects.get_or_create(file_type='widget/rss/text')
        if content_id == -1:
            content_id = None
        widget, created = Content.get_user_widgets(user_details=user_details).update_or_create(
            content_id=content_id, defaults=dict(
                title=title, widget_text=posted_data.get('widget_text'), duration=WIDGET_SCROLL_TIME,
                content_type_id=content_type.content_type_id, organization_id=user_details.organization.organization_id,
                last_updated_by=user_details))
        if created:
            widget.uploaded_by = user_details
            widget.save()
        success = True
    except Exception as e:
        mail_exception(exception=e)
        mail_exception(exception=e)
        errors = ['Invalid widget details']
    return ajax_response(success=success, errors=errors)


def upsert_fb_widget(request):
    debugFileLog.info("Inside upsert fb widget")
    success = False
    errors = []
    try:
        user_details = get_userdetails(request)
        posted_data = string_to_dict(request.body)
        content_id = int(posted_data.get('content_id'))
        title = posted_data.get('title')
        # TODO: Remove this hard-coding of widget/fb/text
        content_type, created = ContentType.objects.get_or_create(file_type='widget/fb/page')
        if content_id == -1:
            content_id = None
        content, created = Content.get_user_widgets(user_details=user_details).update_or_create(
            content_id=content_id, defaults=dict(
                title=title, content_type_id=content_type.content_type_id, 
                organization_id=user_details.organization.organization_id, last_updated_by=user_details,
                ))
        if created:
            content.uploaded_by = user_details
            content.save()
            content_id = content.content_id
        fb_page_url = posted_data.get('fb_page_url')
        if not fb_page_url:
            return ajax_response(success=False, errors=['Invalid FB page url'])

        no_of_posts = int(posted_data.get('no_of_posts')) if posted_data.get('no_of_posts') else FbWidget.default_no_of_posts
        post_duration = int(posted_data.get('post_duration')) if posted_data.get('post_duration') else FbWidget.post_duration
        fb_widget, created = FbWidget.objects.update_or_create(content_id=content_id, defaults=dict(
            fb_page_url=fb_page_url, no_of_posts=no_of_posts, post_duration=post_duration))
        success = True
    except Exception as e:
        mail_exception(exception=e)
        errors = ['Invalid widget details']
    return ajax_response(success=success, errors=errors)


def getFBWidget(request, content_id):
    fb_widget = FbWidget.objects.get(content_id=content_id)
    pageName = FbWidget.get_page_name(fb_widget.fb_page_url)
    context_dic = {}
    noOfPosts = fb_widget.no_of_posts
    [pageExists, posts, postsIds] = checkIfPageExists(pageName, noOfPosts)
    if pageExists :
        context_dic['pageNameInURL'] = pageName
        context_dic['pageName'] = getPageName(pageName)
        context_dic['pagePicture'] = "https://graph.facebook.com/"+ pageName + "/picture"
        context_dic['posts'] = posts
        context_dic['postDuration'] = fb_widget.post_duration
        context_dic['postsIds'] = ','.join(postsIds)
        return render(request, 'widgets/socialMedia/facebook/facebookwidget.html', context_dic)
    else : 
        return ajax_response(success=False)


def check_fb_page_exists(request):
    posted_data = string_to_dict(request.body)
    fb_page_url = posted_data.get('fb_page_url')
    page_name = FbWidget.get_page_name(fb_page_url)
    [success, x, y] = checkIfPageExists(page_name)
    return ajax_response(success=success)


def checkIfPageExists(pageName, noOfPosts=1):
    try:
        graphapiurl = "https://graph.facebook.com/"
        fbAccessToken = "access_token=583412958518077|yxWncaswG-JWQGQwI1MWc04icXY"
        limitposts = "limit="+ str(noOfPosts) 
        rawPosts = urllib2.urlopen(graphapiurl + pageName + "/posts" + '?' + limitposts + '&' + fbAccessToken).read()
        rawPostsAfterJson = json.loads(rawPosts)
        if 'error' in rawPostsAfterJson :
            return [False, False, False]
        else : 
            [postsDetails, postsIds] = getPostDetails(rawPostsAfterJson, noOfPosts)
            return [True, postsDetails, postsIds]
    except Exception as e:
        debugFileLog.error('Error while checking FB page exists')
        debugFileLog.exception(e)
        return [False, False, False]


def getPostDetails(rawPostsAfterJson, noOfPosts):
    graphapiurl = "https://graph.facebook.com/?ids="
    fieldsRequired = "&fields=message,full_picture"
    access_token = "&access_token=583412958518077|yxWncaswG-JWQGQwI1MWc04icXY"
    postsIds = []
    lengthOfAvailablePosts = len(rawPostsAfterJson['data'])
    postsDetails=[]
    if noOfPosts > lengthOfAvailablePosts:
        noOfPosts = lengthOfAvailablePosts
    for i in range(0, noOfPosts):
        postsIds.append(rawPostsAfterJson['data'][i]['id'])
    rawPostsDetails = urllib2.urlopen(graphapiurl + ','.join(postsIds)+fieldsRequired+access_token).read()
    rawPostsDetailsAfterJson = json.loads(rawPostsDetails)
    for i in range(0, noOfPosts):
        post = {}
        if 'message' in rawPostsDetailsAfterJson[postsIds[i]]:
            post['message'] = rawPostsDetailsAfterJson[postsIds[i]]['message']
        if 'full_picture' in rawPostsDetailsAfterJson[postsIds[i]]:
            post['picture'] = rawPostsDetailsAfterJson[postsIds[i]]['full_picture']
        if len(post) > 0 : 
            postsDetails.append(post)
    return [postsDetails, postsIds]


def getPageName(pageName):
    pageNameUrl = 'https://graph.facebook.com/'+pageName+'?access_token=583412958518077|yxWncaswG-JWQGQwI1MWc04icXY'    
    pageName = json.loads(urllib2.urlopen(pageNameUrl).read())['name']
    return pageName
