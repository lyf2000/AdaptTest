from django.shortcuts import render

def index(request):
	return render(request, 'startpage/index.html')

def sign_up(request):
	return render(request, 'startpage/signup.html')
