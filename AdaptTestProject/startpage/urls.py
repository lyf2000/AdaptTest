from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('', views.login, name='index'),
	path('signup/', views.sign_up, name='signup'),
	path('logout/', views.logout, name='logout'),
	path('profile/', views.profile, name='profile'), 
	path('create_test1/', views.create_test1, name='create_test1'),
	path('create_test2/', views.create_test2, name='create_test2'),
	path('test_created_successfully/', views.test_created_successfully, name='test_created_successfully-startpage'),
	path('my_created_tests/', views.my_created_tests, name="my_created_tests"),
	path('tests/', views.tests_page, name="tests"),
	path('all_my_attempts/', views.all_my_attempts, name="all_my_attempts-startpage"), 
	path('test_result/', views.test_result, name="test_result-startpage"),
	path('succes_signup/', views.account_created_successfully, name="succes_signup"),
	path('tests/<int:testid>/start_test/', views.start_test_page, name='start_test'),
	path('tests/<int:testid>/question/', views.question1, name='question')


]