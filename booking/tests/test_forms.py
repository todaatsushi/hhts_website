from django.test import TestCase

from booking.forms import BookTourForm
import booking.tests.helper as h


class BookTourFormTestCase(TestCase):
    def setUp(self):
        self.booking = h.create_booking()
        self.data = self.booking.__dict__

    def test_booking_form_can_validate_valid_info(self):
        del self.data['_state']
        form = BookTourForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_booking_form_can_detect_invalid_data(self):
        del self.data['_state']
        self.data['contact_name'] = None
        form = BookTourForm(data=self.data)
        self.assertFalse(form.is_valid())

