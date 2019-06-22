from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _

from .email_helper import ConfirmEmail

class Booking(models.Model):

    AGE_GROUPS = (
        (_('家族'), _('家族')),
        (_('大人'), _('大人')),
        (_('高齢者'), _('高齢者')),
        (_('子供・思春期'), _('子供・思春期')),
        (_('ミックス'), _('ミックス')),
    )

    TRANSPORT_OPTIONS = (
        (_('使う交通手段'), _('使う交通手段')),
        (_('電車'), _('電車')),
        (_('コーチ'), _('コーチ')),
        (_('自動車・バン'), _('自動車・バン')),
        (_('タクシ'), _('タクシ')),
        (_('その他'), _('他の交通手段は後で伝えてください')),
    )

    contact_name = models.CharField(max_length=50, verbose_name=_('名前'))
    is_group = models.BooleanField(default=True, verbose_name=_('グループ予約'))
    group_name = models.CharField(max_length=100, null=True, verbose_name=_('グループ名前'))
    group_number = models.IntegerField(null=True, verbose_name=_('グループの数'))
    contact_number = models.CharField(max_length=50, verbose_name=_('電話番号'))
    contact_address = models.TextField(verbose_name=_('住所'))
    contact_email = models.EmailField(verbose_name=_('メールアドレス'))
    scheduled_at = models.DateTimeField(verbose_name=_('予定時間'))
    duration = models.CharField(max_length=50, verbose_name=_('期間・分'))
    age_group = models.CharField(max_length=50, choices=AGE_GROUPS, verbose_name=_('年齢層'))
    places_to_visit = models.TextField(verbose_name=_('訪問したい酒蔵'))
    transportation = models.CharField(max_length=50, choices=TRANSPORT_OPTIONS, verbose_name='使う交通手段')
    extra_details = models.TextField(verbose_name=_('他に伝えたい情報'))
    booked_at = models.DateTimeField(default=timezone.now, verbose_name=_('予約をとった時間'))
    confirmed = models.BooleanField(default=False, verbose_name=_('確認されたが'))
    complete = models.BooleanField(default=False, verbose_name=_('完成した'))

    class Meta:
        ordering = ['-scheduled_at', '-booked_at', 'confirmed']

    def __str__(self):
        return f'{self.contact_name}: {self.scheduled_at}'

    def confirm(self):
        email = ConfirmEmail(self)
        email.generate_body()
        email.send()

        self.confirmed = True
        self.save()

    def unconfirm(self):
        self.confirmed = False
        self.save()

    def done(self):
        self.complete = True
        self.save()

    def not_done(self):
        self.complete = False
        self.save()
