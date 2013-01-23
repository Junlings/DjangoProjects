# Create your views here.
from django.shortcuts import *
from models import UserProfile

def profile(request):
    return render_to_response('profile.html',{'request':request})