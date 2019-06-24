from django import forms
from django.contrib.auth.models import User
from django.db.utils import OperationalError
from django.utils.translation import gettext_lazy as _

from .helper import generate_email, validate_emails


class DraftEmailForm(forms.Form):
    """
    Field notes:
        other_recipients is inputted with each email taking up a line and then seperated
        by a comma and new line.
    """
    try:
        everyone = [(user.pk, user) for user in list(User.objects.all())]
        staff_recipients = forms.MultipleChoiceField(choices=everyone, required=False)
    except OperationalError:
        staff_recipients = forms.MultipleChoiceField(choices=[(None, None)], required=False)

    all_staff = forms.BooleanField(initial=False, required=False)
    other_recipients = forms.CharField(widget=forms.Textarea(attrs={'rows':4}), required=False, validators=[validate_emails])
    subject = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    admin_email = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['other_recipients'].help_text = (
            _('各メールは、最後にコンマを入れて、別々の行に入れてください。') +
            f"""
            e.g.
                test@mail.com,*{_('NEWLINE')}*
                test2@mail.com,*{_('NEWLINE')}*
                etc.
            """
        )

    def save_draft(self, request):
        form = generate_email(request, self.cleaned_data)
        form.save()
