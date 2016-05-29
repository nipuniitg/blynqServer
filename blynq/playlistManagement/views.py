from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from contentManagement.models import Content
from contentManagement.serializers import ContentSerializer
from contentManagement.views import get_files_recursively
from customLibrary.views_lib import get_userdetails, string_to_dict, ajax_response, list_to_json
from playlistManagement.models import Playlist, PlaylistItems


# Create your views here.
from playlistManagement.serializers import PlaylistSerializer
from scheduleManagement.models import SchedulePlaylists


@login_required
def index(request):
    return render(request, 'playlistManagement/playlist_index.html')


# This function is for inserting, updating and deleting content from a playlist
def upsert_playlist(request):
    errors = []
    success = False
    user_details = get_userdetails(request)
    try:
        # Extract data from request.body
        posted_data = string_to_dict(request.body)
        playlist_id = int(posted_data.get('playlist_id'))
        playlist_title = posted_data.get('playlist_title')
        playlist_items = posted_data.get('playlist_items')
        user_playlists = Playlist.get_user_relevant_objects(user_details=user_details)

        # upsert playlist
        if playlist_id == -1:
            playlist = Playlist.objects.create(playlist_title=playlist_title, created_by=user_details,
                                               last_updated_by=user_details, organization=user_details.organization)
            playlist_id = playlist.playlist_id
        else:
            playlist = user_playlists.get(playlist_id=playlist_id)
            playlist.playlist_title = playlist_title
            playlist.last_updated_by = user_details
            playlist.save()

        # upsert playlist items
        playlist_total_time = 0
        playlist_item_id_list = []
        for pos_index, item in enumerate(playlist_items):
            playlist_item_id = int(item.get('playlist_item_id'))
            content_id = int(item.get('content_id'))
            display_time = int(item.get('display_time'))
            playlist_total_time = playlist_total_time + display_time
            content = Content.get_user_relevant_objects(user_details=user_details).get(content_id=content_id)
            if playlist_item_id == -1:
                entry = PlaylistItems.objects.create(playlist=playlist, content=content, position_index=pos_index,
                                                     display_time=display_time)
                playlist_item_id = entry.playlist_item_id
            else:
                entry = PlaylistItems.objects.get(playlist_item_id=playlist_item_id)
                entry.position_index = pos_index
                entry.display_time = display_time
                entry.save()
            playlist_item_id_list.append(playlist_item_id)

        playlist.playlist_total_time = playlist_total_time
        playlist.save()

        # Remove content not in playlist_items
        removed_playlist_content = PlaylistItems.objects.filter(playlist=playlist).exclude(
            playlist_item_id__in=playlist_item_id_list)
        for content in removed_playlist_content:
            content.delete()

        # Set the last_updated_time for all the schedules having this playlist
        schedule_playlists = SchedulePlaylists.objects.filter(playlist_id=playlist_id)
        for each_schedule_playlist in schedule_playlists:
            schedule = each_schedule_playlist.schedule
            schedule.save()
        json_data = PlaylistSerializer().serialize([playlist],
                                                   fields=('playlist_id', 'playlist_title', 'playlist_items'))
        assert len(json_data) > 0
        obj_dict = {'playlist': json_data[0]}
        success = True
    except Exception as e:
        print "Exception is ", e
        error = 'Error while upserting content to playlist'
        print error
        errors.append(error)
        obj_dict = None
    return ajax_response(success=success, errors=errors, obj_dict=obj_dict)


def get_playlists(request):
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
    user_playlists = Playlist.get_user_relevant_objects(user_details=user_details)
    json_data = PlaylistSerializer().serialize(user_playlists,
                                               fields=('playlist_id', 'playlist_title','playlist_items'))
    return list_to_json(json_data)

def get_files_recursively_json(request, parent_folder_id):
    """
    :param request:
    :param parent_folder_id:
    :return:
    [
        {
            url: "http://127.0.0.1:8000/media/usercontent/1/fuck_you_bitches.jpg",
            content_id: 1,
            document: "usercontent/1/fuck_you_bitches.jpg",
            title: "fuck_you_bitches"
        }
    ]
    """

    all_files_content_ids = get_files_recursively(request, parent_folder_id=parent_folder_id)
    user_details = get_userdetails(request)
    user_content = Content.get_user_relevant_objects(user_details=user_details)
    all_files = user_content.filter(content_id__in=all_files_content_ids)
    json_data = ContentSerializer().serialize(all_files, fields=('title', 'document', 'document_type', 'content_id'))
    return list_to_json(json_data)


def delete_playlist(request):
    user_details = get_userdetails(request)
    posted_data = string_to_dict(request.body)
    playlist_id = int(posted_data.get('playlist_id'))
    errors = []
    success = False
    try:
        playlist = Playlist.get_user_relevant_objects(user_details=user_details).get(playlist_id=playlist_id)
        playlist.delete()
        success = True
    except Exception as e:
        print "Exception is ", e
        error = "Error while deleting playlist"
        print error
        errors.append(error)
    return ajax_response(success=success, errors=errors)






