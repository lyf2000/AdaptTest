from django.shortcuts import render
from django.http import HttpResponse
from . import views
from startpage.models import *

# Create your views here.

def homepage(request):
	user_name = User.objects.get(id=1).first_name
	out = f'<h1>{user_name}</h1>'
	return HttpResponse(out)


def create_test(request):
	pass



def my_tests(request):
	pass


def pass_test(request):
	pass
