from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('', views.index, name='index-startpage'),
	path('signup/', views.sign_up, name='signup-startpage'),
]