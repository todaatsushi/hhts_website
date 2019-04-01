from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(verbose_name='名称' ,max_length=100)
    content = models.TextField(verbose_name='内容')
    posted_at = models.DateTimeField(verbose_name='投稿時間', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='更新時間', default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='by', verbose_name='著者')
    pinned = models.BooleanField(default=False, verbose_name='重要')
    admin_post = models.BooleanField(default=False, verbose_name='管理者向き')

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def pin(self):
        self.pinned = True
        self.save()

    def unpin(self):
        self.pinned = False
        self.save()

    def admin(self):
        self.admin_post = True
        self.save()

    def unadmin(self):
        self.admin_post = False
        self.save()


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments', verbose_name='ポスト')
    commenter = models.CharField(max_length=50, verbose_name='名前')
    comment = models.TextField(verbose_name='コメント')
    posted_at = models.DateTimeField(default=timezone.now, verbose_name='投稿時間')
    last_updated_at = models.DateTimeField(default=timezone.now, verbose_name='更新時間')
    by_admin = models.BooleanField(default=False, verbose_name='管理者')

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return f"{self.commenter}: {self.comment}"

    def admin(self):
        self.by_admin = True
        self.save()

    def unadmin(self):
        self.by_admin = False
        self.save()
