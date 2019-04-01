from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

from .models import EmailBlast
from .helper import generate_email, validate_emails


class DraftEmailForm(forms.Form):
    everyone = [(user.pk, user) for user in list(User.objects.all())]

    staff_recipients = forms.MultipleChoiceField(choices=everyone, required=False)
    all_staff = forms.BooleanField(initial=False, required=False)
    other_recipients = forms.CharField(widget=forms.Textarea(attrs={'rows':4}), required=False, validators=[validate_emails])
    subject = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    admin_email = forms.BooleanField(initial=False, required=False)

    def save_draft(self, request):
        form = generate_email(request, self.cleaned_data)
        form.save()
