from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from JsonTestData import TestDataClass
from django.http import JsonResponse


# Create your views here.
from customLibrary.views_lib import user_and_organization


@login_required
def index(request):
    return render(request, 'playlistManagement/playlist_index.html')


def getPlaylistsJson(request):
    classObj = TestDataClass()
    playlists = classObj.getPlaylistsTestData()
    return JsonResponse(playlists, safe=False)


def add_playlist(request):
    return render(request, '')


def get_playlist_items(request, playlist_id):
    user_details, organization = user_and_organization(request)

