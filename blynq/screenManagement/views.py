from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
#from models import
# Create your views here.

@login_required
def index(request):
    return render(request,'screen/screen_index.html')
