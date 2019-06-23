from django.test import TestCase
from django.utils import timezone

from booking.forms import BookTourForm
import booking.tests.helper as h


class BookTourFormTestCase(TestCase):
    def setUp(self):
        self.booking = h.create_booking()
        self.data = self.booking.__dict__

    def test_booking_form_can_validate_valid_info(self):
        data = {
            'scheduled_at': timezone.now(),
            'duration': 15, 'places_to_visit': 'a', 'transportation': 'Coach',
            'contact_name': 'a', 'contact_address':
            'a', 'contact_email': '1@m.com',
            'contact_number': '123',
            'is_group': True,
            'group_name': 'a',
            'group_number': 12,
            'age_group': 'Adults',
            'extra_details': 'a'
        }
        form = BookTourForm(data=data)
        self.assertTrue(form.is_valid())

    def test_booking_form_can_detect_invalid_data(self):
        del self.data['_state']
        self.data['contact_name'] = None
        form = BookTourForm(data=self.data)
        self.assertFalse(form.is_valid())
