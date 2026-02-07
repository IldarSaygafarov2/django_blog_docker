from django.db import models
from apps.common.models import BaseTimedModel
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class CategoryModel(BaseTimedModel):
    name = models.CharField(max_length=25, verbose_name='Название')

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('category-posts', kwargs={'pk': self.pk})
    class Meta:
        verbose_name = 'Категория' # name of model in singular
        verbose_name_plural = 'Категории'

class Post(BaseTimedModel):
    name = models.CharField(max_length=50, verbose_name='Заголовок')
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание', blank=True, null=True)
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    preview = models. ImageField(upload_to='articles/previews/', verbose_name='Превью', blank=True, null=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='posts', verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts', verbose_name='Автор')

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']

def make_image_path(instance, filename):
    return f'articles/galleries/post-{instance.post.id}/{filename}'

class PostGalltery(BaseTimedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    photo = models.ImageField(upload_to=make_image_path)


class Comment(BaseTimedModel):
    text = models.TextField(verbose_name='Текст')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Пользователь')

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class PostViewsCount(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

# OneToOneField
# ManyToManyField

class Like(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ManyToManyField(User, related_name='likes')

class Dislike(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ManyToManyField(User, related_name='dislikes')

