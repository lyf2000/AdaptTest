from django.shortcuts import render

#главная страница - вход 
def index(request):
	return render(request, 'startpage/index.html')

#регистрация
def sign_up(request):
	return render(request, 'startpage/signup.html')

#личный кабинет
def profile(request):
	return render(request, 'startpage/profile.html')

#промежуточная страница при создании теста
def create_test1(request):
	return render(request,'startpage/test_creation_first.html')

#страница сооздания теста, где будут вноситься вопросы, варианты ответов и правильный ответы
def create_test2(request):
	return render(request,'startpage/test_creation_first.html')
