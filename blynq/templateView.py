from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

@login_required
def get_shared_partail_templates(request, template_name):
    path = 'Shared/'
    extn = '.html'
    return render(request, (path+template_name+extn))

@login_required
def get_content_partial_templates(request,template_name):
    path = 'ContentManagement/'
    extn = '.html'
    return render(request, (path+template_name+extn))