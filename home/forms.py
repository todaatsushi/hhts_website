from django import forms
from django.utils.translation import gettext_lazy as _

from home.models import Feedback


class ContactForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'name', 'email', 'message',
        ]
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 10,
            }),
        }
