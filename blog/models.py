from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.mail import send_mass_mail

class Post(models.Model):
	title = models.CharField(max_length=100)
	text = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, related_name='posts')
	

	class Meta:
		ordering = ['-date',]
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		url = reverse('ViewPost', args=[self.author.username,
										self.pk])
		return url

	def save(self, *args, **kwargs):
		super(Post, self).save(*args, **kwargs)
		blog = Blog.objects.get(author=self.author)
		users = blog.users.all()
		datalist = []
		for user in users:
			if user.email:
				data = ('Здравствуйте в блоге на который вы подписаны был опубликован пост: ', \
					self.title + '' + self.text + ' ' + 'Ссылка - url_posts', \
					'agent53347@mail.ru', [user.email])
				datalist.append(data)
			send_mass_mail(tuple(datalist))



class Blog(models.Model):
	author = models.OneToOneField(User)
	posts = models.ManyToManyField(Post, blank=True, related_name='posts') #Посты в блоге
	readed = models.ManyToManyField(Post, blank=True, related_name='readed') #Прочитан ли пост 
	users = models.ManyToManyField(User, blank=True, related_name='users') #Подписчики
	blogs_feed = models.ManyToManyField(User,blank=True, related_name='blogs_feed') #Подписки


	def __str__(self):
		return self.author.username
