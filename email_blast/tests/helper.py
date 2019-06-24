from email_blast.models import EmailBlast

from django.contrib.auth.models import User


def create_user():
    """
    Returns a newly created User object that has already been saved in the db.
    """
    return User.objects.create_superuser(
        username='Atsushi',
        email='test@email.com',
        password='tesTing321'
    )


def create_public_email(user):
    """
    Creates and returns EmailBlast for testing.
    """
    return EmailBlast.objects.create(
        subject='Test email',
        recipients="""
            email@mail.com,
            email2@mail.com,
            test@email.com
        """, # includes user's admin email
        content='Test email',
        sender=user
    )

def create_admin_only_email(user):
    """
    Creates and returns EmailBlast for testing.
    """
    return EmailBlast.objects.create(
        subject='Test admin email',
        recipients="""
            email@mail.com,
            email2@mail.com,
            test@email.com
        """,
        content='Test email',
        sender=user,
        is_admin=True
    )