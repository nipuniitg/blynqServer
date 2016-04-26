from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from JsonTestData import TestDataClass
from django.http import JsonResponse, HttpResponse

from contentManagement.models import Content
from customLibrary.views_lib import user_and_organization, string_to_dict, ajax_response
from customLibrary.serializers import FlatJsonSerializer
from playlistManagement.models import Playlist, PlaylistItems


# Create your views here.


@login_required
def index(request):
    return render(request, 'playlistManagement/playlist_index.html')


def add_playlist(request):
    #data in request.body- components passes "title"
    errors = []
    success = False
    user_details, organization = user_and_organization(request)
    try:
        posted_data = string_to_dict(request.body)
        title = posted_data.get('title')
        Playlist.objects.create(title=title,
                                created_by=user_details,
                                last_updated_by=user_details,
                                organization=organization)
        success = True
    except:
        error = 'Error with the submitted data in add playlist'
        print error
        errors.append(error)
    return ajax_response(success=success, errors=errors)


# This function is for inserting, updating and deleting content from a playlist
def upsert_playlist_items(request):
    errors = []
    success = False
    user_details, organization = user_and_organization(request)
    try:
        posted_data = string_to_dict(request.body)
        playlist_id = int(posted_data.get('playlist_id'))
        playlist_items = posted_data.get('playlist_items')
        content_id_list = []
        playlist = Playlist.get_user_relevant_objects(user_details=user_details).get(playlist_id=playlist_id)
        for item in playlist_items:
            # item = item.string_to_dict(item)
            content_id = int(item.get('content_id'))
            content_id_list.append(content_id)
            position_index = int(item.get('position_index'))
            display_time = int(item.get('display_time'))
            content = Content.get_user_relevant_objects(user_details=user_details).get(content_id=content_id)
            entry, created = PlaylistItems.objects.get_or_create(playlist=playlist, content=content,
                                                        defaults={'position_index': position_index,
                                                                  'display_time': display_time})
            if not created:
                entry.position_index = position_index
                entry.display_time = display_time
                entry.save()
        removed_content = PlaylistItems.objects.filter(playlist=playlist).exclude(content__content_id__in=content_id_list)
        for content in removed_content:
            content.delete()
        success = True
    except:
        error = 'Error while upserting content to playlist'
        print error
        errors.append(error)
    return ajax_response(success=success, errors=errors)


def get_playlist_items(request):
    user_details, organization = user_and_organization(request)
    user_playlists = Playlist.get_user_relevant_objects(user_details=user_details)
    json_data = FlatJsonSerializer().serialize(user_playlists, fields=('playlist_id', 'title','playlist_items'))
    return HttpResponse(json_data, content_type='application/json')


def delete_playlist(request):
    user_details, organization = user_and_organization(request)
    posted_data = string_to_dict(request.body)
    playlist_id = int(posted_data.get('playlist_id'))
    errors = []
    success = False
    try:
        playlist = Playlist.get_user_relevant_objects(user_details=user_details).get(playlist_id=playlist_id)
        playlist.delete()
        success=True
    except:
        error = "Error while deleting playlist"
        print error
        errors.append(error)
    return ajax_response(success=success, errors=errors)






