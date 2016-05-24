from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

@login_required
def getSharedPartailtemplate(request, template_name):
    path = 'Shared/'
    extn = '.html'
    return render(request, (path+template_name+extn))