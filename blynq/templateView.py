from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

@login_required
def get_shared_partail_templates(request, template_name):
    path = 'shared/'
    extn = '.html'
    return render(request, (path+template_name+extn))

@login_required
def get_content_partial_templates(request,template_name):
    print 'inside get_content_partial_templates'
    path = 'contentManagement/'
    extn = '.html'
    return render(request, (path+template_name+extn))

def get_screen_partial_templates(request, template_name):
    path = 'screen/'
    extn = '.html'
    return render(request, (path+template_name+extn))

def get_playlist_partial_templates(request, template_name):
    path = 'playlistManagement/'
    extn = '.html'
    return render(request, (path+template_name+extn))
