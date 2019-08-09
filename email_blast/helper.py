from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import EmailBlast


def generate_email(request, cleaned_data):
    """
    Given django form cleaned_data (dict), returns EmailBlast object with processed attributes.
    """

    # Don't send to any non admins if admin email is True
    if cleaned_data.get('admin_email'):
        others_to = []
    else:
        others_to = cleaned_data.get('other_recipients', 'None').split(',\r\n')

    # If email is for every staff member, automatically add their emails
    if cleaned_data.get('all_staff'):
        staff_to = [
            u.email for u in User.objects.all()
        ]
    else:
        # Otherwise only add those who are specified
        staff_to = [
            u.email for u in User.objects.filter(id__in=cleaned_data.get('staff_recipients', ''))
        ]

    # Aggregate all recipients
    all_to = ','.join(staff_to) + ',' if staff_to else ''
    all_to += ','.join(others_to) if others_to else ''
    all_to = all_to.rstrip(',')

    email = EmailBlast(
        subject=cleaned_data.get('subject'),
        recipients=all_to,
        content=cleaned_data.get('content'),
        sender=request.user,
        is_admin=cleaned_data.get('admin_email'),
    )

    return email


def validate_emails(emails):
    """
    Given a string of emails seperated by ',', checks each email using regex
    to test for validity, returning True if all are valid, else False.
    """
    import re

    email_list = emails.split(',')
    email_re = r"[^@]+@[^@]+\.[^@]+"

    for address in email_list:
        if not re.match(email_re, address):
            raise ValidationError(
                f'{address} is not valid!',
                code='invalid'
            )

    return True
