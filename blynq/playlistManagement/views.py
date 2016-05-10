from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from JsonTestData import TestDataClass
from django.http import JsonResponse, HttpResponse

from contentManagement.models import Content
from contentManagement.views import get_files_recursively
from customLibrary.views_lib import get_userdetails, string_to_dict, ajax_response
from customLibrary.serializers import FlatJsonSerializer, playlist_dict
from playlistManagement.models import Playlist, PlaylistItems


# Create your views here.


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
        playlist_item_id_list = []
        for pos_index, item in enumerate(playlist_items):
            playlist_item_id = int(item.get('playlist_item_id'))
            content_id = int(item.get('content_id'))
            display_time = int(item.get('display_time'))
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

        # Remove content not in playlist_items
        removed_playlist_content = PlaylistItems.objects.filter(playlist=playlist).exclude(
            playlist_item_id__in=playlist_item_id_list)
        for content in removed_playlist_content:
            content.delete()
        obj_dict = {'playlist': playlist_dict(playlist)}
        success = True
    except:
        error = 'Error while upserting content to playlist'
        print error
        errors.append(error)
        obj_dict = None
    return ajax_response(success=success, errors=errors, obj_dict=obj_dict)


def get_playlists(request):
    user_details = get_userdetails(request)
    user_playlists = Playlist.get_user_relevant_objects(user_details=user_details)
    json_data = FlatJsonSerializer().serialize(user_playlists,
                                               fields=('playlist_id', 'playlist_title','playlist_items'))
    return HttpResponse(json_data, content_type='application/json')


def get_files_recursively_json(request, parent_folder_id):
    all_files_content_ids = get_files_recursively(request, parent_folder_id=parent_folder_id)
    user_details = get_userdetails(request)
    user_content = Content.get_user_relevant_objects(user_details=user_details)
    all_files = user_content.filter(content_id__in=all_files_content_ids)
    json_content = FlatJsonSerializer().serialize(all_files, fields=('title', 'document', 'content_id'))
    return HttpResponse(json_content, content_type='application/json')


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
    except:
        error = "Error while deleting playlist"
        print error
        errors.append(error)
    return ajax_response(success=success, errors=errors)






