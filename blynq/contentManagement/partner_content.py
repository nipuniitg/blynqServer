import os
from os import listdir
from os.path import isfile, join, exists, isdir

from authentication.models import Organization, UserDetails
from blynq.settings import CONTENT_ORGANIZATION_NAME
from contentManagement.models import Content
from contentManagement.views import process_media
from customLibrary.views_lib import debugFileLog

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
            output = process_media(file_path=file_path, parent_folder=parent_folder, user_details=user_details,
                                   organization=organization)
            if output:
                print 'Successfully uploaded %s' % file_path
            else:
                print 'Uploading file unsuccessful %s ' % file_path
    except Exception as e:
        debugFileLog.exception(e)
        debugFileLog.exception('Exception while processing %s ' % file_path)


def get_or_create_directory(title, parent_folder, user_details, organization):
    dir_obj, created = Content.objects.get_or_create(title=title, organization=organization, is_folder=True,
                                                     parent_folder=parent_folder, uploaded_by=user_details,
                                                     last_modified_by=user_details)
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


def push_content():
    try:
        organization, created = Organization.objects.get_or_create(
            organization__organization_name=CONTENT_ORGANIZATION_NAME)
        user_details = UserDetails.objects.get(organization=organization)
        parent_folder = None
        if not exists(DOWNLOADED_PARTNER_DIRECTORY):
            print 'Downloaded partner directory %s does not exist' % DOWNLOADED_PARTNER_DIRECTORY
            return
        path = DOWNLOADED_PARTNER_DIRECTORY
        process_directory(path=path, organization=organization, user_details=user_details, parent_folder=parent_folder)
    except Exception as e:
        debugFileLog.exception('Exception while calling fetch_content')
        debugFileLog.exception(e)
    print 'All the downloaded partner content has been uploaded successfully'
