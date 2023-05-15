from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.


class PostType(models.Model):
    name = models.CharField("Name", max_length=100)
    url = models.SlugField(max_length=160, unique=True)
    objects = models.Manager()
    def __str__(self):
        return self.name

class PostCategory(models.Model):
    name = models.CharField("Name", max_length=100)
    image = models.ImageField(upload_to='post/category')
    url = models.SlugField(max_length=160, unique=True)
    objects = models.Manager()
    def __str__(self):
        return self.name

class Post(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, db_index=True, unique=True)
    description = models.TextField(max_length=200, db_index=True)
    date = models.DateTimeField('Date')
    type = models.ManyToManyField(PostType, verbose_name="type")
    category = models.ManyToManyField(PostCategory, verbose_name="category")
    screen = models.ManyToManyField('PostScreenshot', related_name='post_images')
    file = models.ManyToManyField('PostFile', related_name='post_files')
    objects = models.Manager()
    def get_absolute_url(self):
        return reverse('main:post', args = [self.id, self.slug])

class PostScreenshot(models.Model):
    screenshot = models.ImageField(upload_to='post/image')
    post_screen = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_screenshots')

class PostFile(models.Model):
    post_file = models.FileField(upload_to='post/files')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_files')

class Comments(models.Model):
    user = models.CharField(max_length=20, db_index=True)
    text = models.TextField(max_length=300, db_index=True)
    post = models.ForeignKey(Post, related_name='comment', on_delete = models.CASCADE, null=True, default=None)
    date = models.DateTimeField('Date', default=timezone.now, null=True)
    def __str__(self):
        return f"{self.user} - {self.text}"

class User(AbstractUser):
    pass