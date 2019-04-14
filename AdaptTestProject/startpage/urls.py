from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('', views.index, name='index-startpage'),
	path('signup/', views.sign_up, name='signup-startpage'),
	path('profile/', views.profile, name='profile-startpage'), 
	path('test_creation_first/', views.create_test1, name='test_creation_first-startpage'),
	path('test_creation_second/', views.create_test2, name='test_creation_second-startpage')
]