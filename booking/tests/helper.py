from django.utils import timezone

import os

from booking.models import Booking


def create_booking():
    """
    Returns test Booking obj.
    """
    return Booking.objects.create(
        contact_name='Me',
        is_group=True,
        group_name='Fast 5',
        group_number=10,
        contact_number=12345,
        contact_address='Rio',
        contact_email=os.environ.get('GMAIL_ADDRESS'),
        scheduled_at=timezone.now(),
        duration='60',
        age_group='ミックス',
        places_to_visit='All of them',
        transportation='自動車・バン',
        extra_details=None,
        booked_at=timezone.now(),
        confirmed=False,
        complete=False
    )