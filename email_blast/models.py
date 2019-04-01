from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class EmailBlast(models.Model):
    subject = models.CharField(max_length=100, verbose_name='件名')
    recipients = models.TextField(verbose_name='受取人のメールアドレス')
    content = models.TextField(verbose_name='内容')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='送り人')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='書き時間')
    last_updated_at = models.DateTimeField(default=timezone.now, verbose_name='更新時間')
    sent_at = models.DateTimeField(default=None, null=True, verbose_name='送り時間')
    is_admin = models.BooleanField(default=False, verbose_name='管理者向き')
    sent = models.BooleanField(default=False, verbose_name='送った')

    class Meta:
        ordering = ['-last_updated_at', '-created_at', '-sent_at']

    def __str__(self):
        return self.subject

    def __repr__(self):
        return f'{self.subject}, from {self.sender} at {self.sent_at}'

    def mark_admin(self):
        self.is_admin = True
        self.save()

    def unmark_admin(self):
        self.is_admin = False
        self.save()

    def mark_sent(self):
        self.sent = True
        self.sent_at = timezone.now()
        self.save()
