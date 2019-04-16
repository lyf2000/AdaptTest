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
	return render(request,'startpage/test_creation_second.html')

def test_created_successfully(request):
	return render(request, 'startpage/test_created_successfully.html')

def my_created_tests(request):
	return render(request, 'startpage/my_created_tests.html')

def tests_page(request):
	return render(request, 'startpage/tests_page.html')

def all_my_attempts(request):
	return render(request, 'startpage/all_my_attempts.html')

def test_result(request):
	return render(request, 'startpage/test_result.html')

def start_test(request):
	return render(request, 'startpage/start_test.html')

def question(request):
	return render(request, 'startpage/question.html')