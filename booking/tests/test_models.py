from django.test import TestCase

import booking.tests.helper as h
from booking.models import Booking


class BookingTestCase(TestCase):

    def setUp(self):
        self.booking = h.create_booking()

    def test_can_make_booking(self):
        self.assertIsInstance(self.booking, Booking)
        self.assertEqual(self.booking.__str__(), f'{self.booking.contact_name}: {self.booking.scheduled_at}')

    def test_mark_booking_as_doneand_not_done(self):
        self.assertFalse(self.booking.complete)
        self.booking.done()
        self.assertTrue(self.booking.complete)
        self.booking.not_done()
        self.assertFalse(self.booking.complete)

    def test_confirming_booking_marks_as_confirmed_and_sends_email(self):
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'):
            self.assertFalse(self.booking.confirmed)
            self.booking.confirm()
            # Check console to see if correct email has been sent.

            self.assertTrue(self.booking.confirmed)

            self.booking.unconfirm()
            self.assertFalse(self.booking.confirmed)
