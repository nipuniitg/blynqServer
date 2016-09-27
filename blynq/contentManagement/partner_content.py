import os
from os import listdir
from os.path import isfile, join, exists, isdir

import datetime

import requests
from django.utils import timezone

from authentication.models import Organization, UserDetails
from blynq.settings import CONTENT_ORGANIZATION_NAME
from contentManagement.models import Content
from contentManagement.views import process_media
from customLibrary.views_lib import debugFileLog, get_ist_datetime, date_to_string, ajax_response

DOWNLOADED_PARTNER_DIRECTORY = '/home/django/partner/'


def process_file(file_path, parent_folder, user_details, organization):
    try:
        filename = os.path.basename(file_path)
        title, ext = os.path.splitext(filename)
        try:
            content = Content.get_user_relevant_objects(user_details).get(
                title__icontains=title, parent_folder=parent_folder, organization=organization)
            print 'File %s already exists in the portal' % file_path
        except Exception as e:
            print 'File %s does not already exist' % title
            conversion_success, delete_old = process_media(file_path=file_path, parent_folder=parent_folder,
                                                           user_details=user_details, organization=organization,
                                                           content_already_saved=False)
            if conversion_success:
                print 'Successfully uploaded %s' % file_path
            else:
                print 'Uploading file unsuccessful %s ' % file_path
            if delete_old:
                os.remove(file_path)
    except Exception as e:
        debugFileLog.exception(e)
        debugFileLog.exception('Exception while processing %s ' % file_path)


def get_or_create_directory(title, parent_folder, user_details, organization):
    dir_obj, created = Content.objects.get_or_create(title=title, organization=organization, is_folder=True,
                                                     parent_folder=parent_folder, uploaded_by=user_details,
                                                     last_updated_by=user_details)
    return dir_obj


def process_directory(path, organization, user_details, parent_folder):
    for partner_file in listdir(path):
        child = join(path, partner_file)
        if isdir(child):
            dir_obj = get_or_create_directory(title=partner_file, parent_folder=parent_folder,
                                              user_details=user_details, organization=organization)
            process_directory(child, organization, user_details, parent_folder=dir_obj)
        elif isfile(child):
            # Ignore hidden files
            if not partner_file.startswith('.'):
                process_file(file_path=child, parent_folder=parent_folder, user_details=user_details,
                             organization=organization)
        else:
            print 'This is not a file or directory. Ignore.'


def content_partner_organization():
    organization, created = Organization.objects.get_or_create(organization_name=CONTENT_ORGANIZATION_NAME)
    if created:
        debugFileLog.error('Organization did not exist previously, just created the %s organization, '
                           'now create a new user' % CONTENT_ORGANIZATION_NAME)
    return organization


def push_content():
    try:
        organization = content_partner_organization()
        user_details = UserDetails.objects.get(organization=organization)
        parent_folder = None
        if not exists(DOWNLOADED_PARTNER_DIRECTORY):
            print 'Downloaded partner directory %s does not exist' % DOWNLOADED_PARTNER_DIRECTORY
            return
        path = DOWNLOADED_PARTNER_DIRECTORY
        process_directory(path=path, organization=organization, user_details=user_details, parent_folder=parent_folder)
    except Exception as e:
        debugFileLog.exception('Exception while calling push_content')
        debugFileLog.exception(e)
    print 'All the downloaded partner content has been uploaded successfully'


def generate_way2_url(category):
    base_way2_url = 'http://www.way2news.co/postsway2?lang=eng'
    way2_date_fmt = "%Y-%m-%d %H:%M:%S"
    ttime = timezone.now()
    ftime = ttime - datetime.timedelta(days=1)
    ttime = get_ist_datetime(ttime)
    ftime = get_ist_datetime(ftime)
    ttime_url_part = '&ttime=' + date_to_string(ttime, fmt=way2_date_fmt)
    ftime_url_part = '&ftime=' + date_to_string(ftime, fmt=way2_date_fmt)
    way2_categories = {'latest': 0, 'news': 81, 'business': 6, 'sports': 15, 'cinema': 8, 'special': 82}
    try:
        category_url_part = '&catid=' + str(way2_categories[category])
    except Exception as e:
        debugFileLog.exception(e)
        category_url_part = '&catid=0'
    return base_way2_url + category_url_part + ftime_url_part + ttime_url_part


WAY2_CONSTANTS = {'playlist_title': 'News', 'folder_title': 'Way2News', 'category': 'latest'}


def process_way2_urls(way2_dict, way2_items_required, time_for_each_url):
    organization = content_partner_organization()
    from playlistManagement.models import Playlist, PlaylistItems
    news_playlist, created = Playlist.objects.get_or_create(playlist_title=WAY2_CONSTANTS['playlist_title'],
                                                            organization=organization)
    parent_folder, created = Content.objects.filter(organization=organization, is_folder=True).get_or_create(
        title=WAY2_CONSTANTS['folder_title'], defaults=dict(organization=organization, is_folder=True))
    count = 0
    content_objs = []
    content_ids = []
    for obj in way2_dict:
        url = obj.get('url')
        title = obj.get('title')
        if url and title:
            count += 1
            if count > way2_items_required:
                break

            content_dict = dict(title=title, parent_folder=parent_folder, duration=time_for_each_url,
                                organization=organization)
            instance, created = Content.objects.filter(organization=organization).get_or_create(url=url,
                                                                                                defaults=content_dict)
            content_ids.append(instance.content_id)
            content_objs.append(instance)
    obsolete_playlist_items = PlaylistItems.objects.filter(playlist=news_playlist).exclude(content_id__in=content_ids)
    if count > way2_items_required:
        obsolete_content_ids = obsolete_playlist_items.values_list('content_id', flat=True)
        obsolete_contents = Content.objects.filter(organization=organization, content_id__in=obsolete_content_ids)
        obsolete_contents.delete()
    else:
        obsolete_playlist_items.delete()
    for obj in content_objs:
        item, created = PlaylistItems.objects.get_or_create(
            content=obj, defaults=dict(playlist=news_playlist, display_time=time_for_each_url))


def fetch_way2news():
    try:
        final_url = generate_way2_url(category=WAY2_CONSTANTS['category'])
        time_for_each_url = 30
        total_time_for_way2 = 600  # 10 minutes
        way2_items_required = total_time_for_way2/time_for_each_url
        result = requests.get(final_url)
        if result.status_code == 200:
            success = True
            way2_dict = result.json()
            if type(way2_dict) is list:
                process_way2_urls(way2_dict, way2_items_required, time_for_each_url)
            elif type(way2_dict) is tuple:
                debugFileLog.exception('Received a tuple from way2 url, %s' % str(way2_dict))
            else:
                debugFileLog.exception('Received unknown response from way2 url')
        else:
            debugFileLog.exception(result.reason)
            debugFileLog.exception('Error while fetching way2 content status code %d , reason %s' %
                                   (result.status_code, result.reason))
            success = False
    except Exception as e:
        debugFileLog.exception(e)
        success = False
    return ajax_response(success=success)