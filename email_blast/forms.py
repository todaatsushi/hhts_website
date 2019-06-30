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
        staff_recipients = forms.MultipleChoiceField(choices=everyone, required=False, label=_('スタッフからの受取人'))
    except OperationalError:
        staff_recipients = forms.MultipleChoiceField(choices=[(None, None)], required=False, label=_('スタッフからの受取人'))

    all_staff = forms.BooleanField(initial=False, required=False, label=_('全スタッフ'))
    other_recipients = forms.CharField(widget=forms.Textarea(attrs={'rows':4}), required=False, validators=[validate_emails], label=_('他の受取人'))
    subject = forms.CharField(max_length=100, label=_('件名'))
    content = forms.CharField(widget=forms.Textarea, label=_('内容'))
    admin_email = forms.BooleanField(initial=False, required=False, label=_('スタッフ専用'))

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
