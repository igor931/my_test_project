from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout
from django.views.generic import ListView, DetailView
from .models import Blog, Post

urlpatterns = [
	url(r'^post_add/$', views.post_add.as_view(), name='post_add'),
	url(r'^login/$', login, name='login'),
	url(r'^logout/$', logout, name='logout'),
	url(r'^$', ListView.as_view(model=Blog, template_name='index.html'), name='index'),
	url(r'^news_feed/$', views.news_feed.as_view(), name='news_feed'),
	url(r'^(?P<username>[-\w]+)/$', views.blog.as_view(), name='blog'),
	url(r'^(?P<username>[-\w]+)/(?P<pk>[0-9]+)/$', DetailView.as_view(model=Post, template_name='detail.html'), name='post'),
	url(r'^(?P<username>[-\w]+)/subscription/$', views.subs.as_view(), name='subs'),
	url(r'^(?P<username>[-\w]+)/unsubscription/$', views.unsubs.as_view(), name='unsubs'),
	url(r'^news_feed/$', views.news_feed.as_view(), name='news_feed'),
	url(r'^readed/post/(?P<post_id>\d+)/$', views.readed.as_view(), name='readed'),

	
#	url(r'^blog_list', ListView.as_view(model=Blog), name='blog_list'),

	]