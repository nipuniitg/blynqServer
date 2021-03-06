from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from contentManagement.models import Content
from contentManagement.serializers import default_content_serializer
from contentManagement.views import get_files_recursively
from customLibrary.views_lib import get_userdetails, string_to_dict, ajax_response, obj_to_json_response, debugFileLog, \
    mail_exception
from playlistManagement.models import Playlist, PlaylistItems
from playlistManagement.serializers import default_playlist_serializer, PlaylistSerializer

# Create your views here.


@login_required
def index(request):
    return render(request, 'playlistManagement/playlist_index.html')


# This function is for inserting, updating and deleting content from a playlist
@transaction.atomic
@login_required
def upsert_playlist(request):
    errors = []
    success = False
    user_details = get_userdetails(request)
    try:
        with transaction.atomic():
            # Extract data from request.body
            posted_data = string_to_dict(request.body)
            playlist = Playlist.upsert_playlist_from_dict(playlist_dict=posted_data, user_details=user_details)
            json_data = default_playlist_serializer([playlist])
            # assert len(json_data) > 0
            if len(json_data) > 0:
                obj_dict = {'playlist': json_data[0]}
            else:
                raise Exception('Playlist Serializer returns empty data')
            success = True
    except Exception as e:
        success = False
        error = 'Error while upserting content to playlist'
        debugFileLog.exception(error)
        mail_exception(exception=e)
        errors.append(error)
        obj_dict = None
    return ajax_response(success=success, errors=errors, obj_dict=obj_dict)


def delete_playlist(request):
    user_details = get_userdetails(request)
    posted_data = string_to_dict(request.body)
    playlist_id = int(posted_data.get('playlist_id'))
    errors = []
    success = False
    try:
        playlist = Playlist.get_user_visible_objects(user_details=user_details).get(playlist_id=playlist_id)
        playlist.delete()
        success = True
    except Exception as e:
        error = "Error while deleting playlist"
        debugFileLog.exception(error)
        mail_exception(exception=e)
        errors.append(error)
    return ajax_response(success=success, errors=errors)


def get_user_playlists(request):
    """
    :param request:
    :return:
    [
        {
            playlist_items: [
                {
                    display_time: 15,
                    title: "sachin",
                    url: "http://127.0.0.1:8000/media/usercontent/1/sachin.jpg",
                    playlist_item_id: 3,
                    is_folder: false,
                    content_id: 3
                },
                {
                    display_time: 15,
                    title: "sachin",
                    url: "http://127.0.0.1:8000/media/usercontent/1/sachin.jpg",
                    playlist_item_id: 4,
                    is_folder: false,
                    content_id: 3
                }
            ],
            playlist_id: 1,
            playlist_title: "first playlist"
        }
    ]
    """
    user_details = get_userdetails(request)
    user_playlists = Playlist.get_user_visible_objects(user_details=user_details)
    json_data = default_playlist_serializer(user_playlists)
    return obj_to_json_response(json_data)


def get_widget_playlists(request):
    user_details = get_userdetails(request)
    user_playlists = Playlist.get_user_invisible_playlists(user_details=user_details)
    json_data = default_playlist_serializer(user_playlists)
    return obj_to_json_response(json_data)


def get_blynq_playlists(request):
    user_details = get_userdetails(request)
    blynq_playlists = Playlist.get_blynq_content_playlists()
    json_data = default_playlist_serializer(blynq_playlists)
    return obj_to_json_response(json_data)


def get_files_recursively_json(request, parent_folder_id):
    """
    :param request:
    :param parent_folder_id:
    :return:
    [
        {
            url: "http://127.0.0.1:8000/media/usercontent/1/sachin.jpg",
            content_id: 1,
            document: "usercontent/1/sachin.jpg",
            title: "sachin"
        }
    ]
    """

    all_files_content_ids = get_files_recursively(request, parent_folder_id=parent_folder_id)
    user_details = get_userdetails(request)
    user_content = Content.get_user_filesystem(user_details=user_details)
    all_files = user_content.filter(content_id__in=all_files_content_ids)
    json_data = default_content_serializer(all_files)
    return obj_to_json_response(json_data)
