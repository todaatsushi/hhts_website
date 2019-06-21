from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Post, Comment


class CommentPostForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['commenter', 'comment']
        labels = {
            'commenter': '名前',
            'comment': 'コメント',
        }


class CommentDeleteForm(forms.ModelForm):
    confirm = forms.BooleanField()

    class Meta:
        model = Comment
        fields = ['confirm']
        labels = {
            'confirm': '確認',
        }
