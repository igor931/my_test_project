from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.models import User
from django.views.generic import ListView
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import PostForm
		
class blog(TemplateView):
	def get(self, request, username):
		template_name = 'blog.html'
		author = User.objects.get(username=username)
		posts = Post.objects.filter(author=author)
		readers = Blog.objects.get(author=request.user)
		blog_user = Blog.objects.get(author=author)
		username=username
		subscription = False
		if request.user in blog_user.users.all():
			subscription = True
		context = {'posts': posts, 'subscription':subscription, 'author':author, 'username':username}
		return render(request, template_name, context)

class subs(View):
	def get(self, request, username):
		blog_user = User.objects.get(username=username) #Автор блога
		read_user = User.objects.get(username=request.user.username) #Читатель блога
		blog_read = Blog.objects.get(author=read_user) #Обьект Блога читателя	
		blog = Blog.objects.get(author=blog_user) #Обьект блога автора
		blog.users.add(read_user)
		blog_read.blogs_feed.add(blog_user)
		return redirect('/blog/')

class unsubs(View):
	def get(self, request, username):
		blog_user = User.objects.get(username=username)
		read_user = User.objects.get(username=request.user.username)
		blog_read = Blog.objects.get(author=read_user)
		blog = Blog.objects.get(author=blog_user)
		blog.users.remove(read_user)
		blog_read.blogs_feed.remove(blog_user)
		for post in blog_user.posts.all():
			blog_read.posts.remove(post)

		return redirect('/blog/')

class news_feed(TemplateView):
	def get(self, request):
		template_name = 'news_feed.html'
		user = request.user
		blog = Blog.objects.get(author=user)
		is_reading = blog.readed.all()

		users_list = blog.blogs_feed.all()
		for user in users_list:
			for post in user.posts.all():
				blog.posts.add(post)
		post_list = blog.posts.all().order_by('-date',)
		context = {'post_list': post_list,'is_reading': is_reading}
		return render(request, template_name, context)

class readed(View):
	def get(self, request, post_id):
		post = Post.objects.get(pk=post_id)
		read_user = Blog.objects.get(author=request.user)
		read_user.readed.add(post)
		return redirect('/blog/news_feed/')

class post_add(FormView):
	def post(self, request):
		template_name = 'post_add.html'
		author = request.user
		title = request.POST.get('title', '')
		text = request.POST.get('text', '')
		post = Post(author=author, text=text)
		post.save()
		return redirect('/')

	def get(self, request):
		template_name = 'post_add.html'
		form = PostForm
		context = {'form': form}
		return render(request, template_name, context)