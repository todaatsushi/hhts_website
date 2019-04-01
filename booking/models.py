from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import EmailMessage

from .email_helper import ConfirmEmail

class Booking(models.Model):

    AGE_GROUPS = (
        ("家族", "家族"),
        ("大人", "大人"),
        ("高齢者", "高齢者"),
        ("子供・思春期", "子供・思春期"),
        ("ミックス", "ミックス"),
    )

    TRANSPORT_OPTIONS = (
        ('使う交通手段', '使う交通手段'),
        ('電車', '電車'),
        ('コーチ', 'コーチ'),
        ('自動車・バン', '自動車・バン'),
        ('タクシ', 'タクシ'),
        ('その他', '他の交通手段（”他に伝えたい情報”で伝えてください。）'),
    )

    contact_name = models.CharField(max_length=50, verbose_name='名前')
    is_group = models.BooleanField(default=True, verbose_name='グループ予約')
    group_name = models.CharField(max_length=100, null=True, verbose_name='グループ名前')
    group_number = models.IntegerField(null=True, verbose_name='グループの数')
    contact_number = models.CharField(max_length=50, verbose_name='電話番号')
    contact_address = models.TextField(verbose_name='住所')
    contact_email = models.EmailField(verbose_name='メールアドレス')
    scheduled_at = models.DateTimeField(verbose_name='予定時間')
    duration = models.CharField(max_length=50, verbose_name='期間（分）')
    age_group = models.CharField(max_length=50, choices=AGE_GROUPS, verbose_name='年齢層')
    places_to_visit = models.TextField(verbose_name='訪問したい酒蔵')
    transportation = models.CharField(max_length=50, choices=TRANSPORT_OPTIONS, verbose_name='使う交通手段')
    extra_details = models.TextField(verbose_name='他に伝えたい情報')
    booked_at = models.DateTimeField(default=timezone.now, verbose_name='予約をとった時間')
    confirmed = models.BooleanField(default=False, verbose_name='確認されたが')
    complete = models.BooleanField(default=False, verbose_name='完成した')

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
