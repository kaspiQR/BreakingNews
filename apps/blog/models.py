from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class News(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='news/')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    @property
    def likes(self):
        return self.news_like.all().count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news_like')

    def __str__(self):
        return self.user.username


# like
# id  | user_id | news_id |
# 1   |   2     | 34      |
# 2   |   3     | 34      |
# 3   |   4     | 34      |
# 4   |   5     | 34      |
# select count(*) from like where news_id = 34; # 4
