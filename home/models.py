from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('名前'))
    email = models.CharField(max_length=100, verbose_name=_('メールアドレス'))
    message = models.TextField(verbose_name=_('メッセージ'))
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Feedback {self.name} @ {self.datetime}'

    def __repr__(self):
        return f'Feedback {self.name} @ {self.datetime}'
