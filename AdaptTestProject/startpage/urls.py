from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('', views.login, name='index'),
	path('signup/', views.sign_up, name='signup'),
	path('logout/', views.logout, name='logout'),
	path('profile/', views.profile, name='profile'), 
	path('create_test1/', views.create_test1, name='test_creation_first-startpage'),
	path('create_test2/', views.create_test2, name='test_creation_second-startpage'),
	path('test_created_successfully/', views.test_created_successfully, name='test_created_successfully-startpage'),
	path('my_created_tests/', views.my_created_tests, name="my_created_tests-startpage"), 
	path('tests_page/', views.tests_page, name="tests_page-startpage"),
	path('all_my_attempts/', views.all_my_attempts, name="all_my_attempts-startpage"), 
	path('test_result/', views.test_result, name="test_result-startpage"), 
	path('start_test/', views.start_test, name="start_test-startpage"), 
	path('question/', views.question, name="question-startpage")
]