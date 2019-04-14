from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('', views.homepage, name='userpage-homepage'),
	path('create/', views.create_test, name='userpage-create_test'),
	path('mytests/', views.my_tests, name='userpage-my_tests'),
	path('pass/', views.pass_test, name='userpage-pass_test'),
]