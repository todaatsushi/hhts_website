from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Post, Comment


class CommentPostForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['commenter', 'comment']
        labels = {
            'commenter': _('名前'),
            'comment': _('コメント'),
        }


class CommentDeleteForm(forms.ModelForm):
    confirm = forms.BooleanField()

    class Meta:
        model = Comment
        fields = ['confirm']
        labels = {
            'confirm': _('確認'),
        }
