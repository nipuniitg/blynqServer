from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from JsonTestData import TestDataClass
from django.http import JsonResponse


# Create your views here.

@login_required
def index(request):
    return render(request, 'playlistManagement/playlist_index.html')


def getPlaylistsJson(request):
    classObj = TestDataClass()
    playlists = classObj.getPlaylistsTestData()
    return JsonResponse(playlists, safe=False)
