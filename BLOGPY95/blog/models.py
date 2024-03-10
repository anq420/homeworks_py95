from django.db import models
from django.conf import settings


class News(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, max_length=120, null=False, blank=False, default='user',
                               on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/images', blank=True, null=True, default='static/images/img.png')
    title = models.CharField(max_length=128, null=False, blank=False, unique=True)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}, {self.content}, {self.image}'

    class Meta:
        verbose_name_plural = 'News'


class Comment(models.Model):
    nickname = models.CharField(max_length=128)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='comments_news')

    def __str__(self):
        return f'{self.nickname}, {self.content}'
