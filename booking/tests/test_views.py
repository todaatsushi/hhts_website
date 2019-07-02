from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from booking.models import Booking
import booking.tests.helper as h
import blog.tests.helper as hb


class BookingViewsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.booking = h.create_booking()
        self.user = hb.create_user()

    def english_setting(self):
        return self.settings(LANGUAGE_CODE='en')

    def test_all_bookings_view(self):
        h.basic_view_check(
            test_case_obj=self,
            path=reverse('booking-index'),
            template='booking/index.html',
            login_required=True,
            login_desired=True,
            text_on_page=[
                '全て', # Japanese text
                'Me', # Booking itself
            ]
        )

    def test_all_bookings_view_en(self):
        with self.english_setting():
            h.basic_view_check(
                self,
                reverse('booking-index'),
                'booking/index.html',
                True,
                True,
                [
                    'All', # Japanese text
                    'Me', # Booking itself
                ]
            )

    def test_book_tour_create_view(self):
        h.basic_view_check(
            self,
            reverse('booking-book'),
            'booking/book_tour.html',
            True,
            True,
            [
                'ツアーを予約', # Japanese text
                '基本情報' # form in japanese
            ]
        )

    def test_book_tour_create_view_en(self):
        with self.english_setting():
            h.basic_view_check(
                self,
                reverse('booking-book'),
                'booking/book_tour.html',
                True,
                True,
                [
                    'Book a tour', # English text
                    'Basic information' # form in english
                ]
            )
    
    def test_booking_detail_view(self):
        h.basic_view_check(
            self,
            reverse('booking-detail', kwargs={'pk': self.booking.pk}),
            'booking/booking_view.html',
            True,
            True,
            [
                self.booking.contact_name,
                '連絡先' # Subtitle
            ]
        )

    def test_booking_detail_view_en(self):
        with self.english_setting():
            h.basic_view_check(
                self,
                reverse('booking-detail', kwargs={'pk': self.booking.pk}),
                'booking/booking_view.html',
                True,
                True,
                [
                    self.booking.contact_name,
                    'Contact information'
                ]
            )

    def test_booking_update_view(self):
        h.basic_view_check(
            self,
            reverse('booking-update', kwargs={'pk': self.booking.pk}),
            'booking/update.html',
            True,
            True,
            [
                'ツアー更新',
                '予定時間' # Subtitle
            ]
        )

    def test_booking_update_view_en(self):
        with self.english_setting():
            h.basic_view_check(
                self,
                reverse('booking-update', kwargs={'pk': self.booking.pk}),
                'booking/update.html',
                True,
                True,
                [
                    'Update booking',
                    'Booking time' # Subtitle
                ]
            )

    def test_booking_delete_view(self):
        h.basic_view_check(
            self,
            reverse('booking-delete', kwargs={'pk': self.booking.pk}),
            'booking/confirm_delete.html',
            True,
            True,
            [
                'ツアーのカンセル',
                '確認' # Confirm button text
            ]
        )

    def test_booking_delete_view_en(self):
        with self.english_setting():
            h.basic_view_check(
                self,
                reverse('booking-delete', kwargs={'pk': self.booking.pk}),
                'booking/confirm_delete.html',
                True,
                True,
                [
                    'Cancel tour',
                    'Confirm'
                ]
            )

    def test_booking_confirm_view(self):
        with self.settings(
            EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
        ):
            self.client.force_login(self.user)
            self.assertFalse(self.booking.confirmed)
            response = self.client.post(reverse('booking-confirm', kwargs={'pk': self.booking.pk}))
            self.assertEqual(response.status_code, 302) # Check terminal for email sent confirmation.

            # Check actual booking
            self.assertTrue(Booking.objects.get(pk=self.booking.pk).confirmed)

            # Test unconfirm
            response_unconfirm = self.client.get(reverse('booking-unconfirm', kwargs={'pk': self.booking.pk}))
            self.assertEqual(response_unconfirm.status_code, 302)

            self.assertFalse(Booking.objects.get(pk=self.booking.pk).confirmed)

    def test_booking_complete_view(self):
        self.client.force_login(self.user)

        self.assertFalse(self.booking.complete)
        response = self.client.get(reverse('booking-complete', kwargs={'pk': self.booking.pk}))
        self.assertEqual(response.status_code, 302)

        self.assertTrue(Booking.objects.get(pk=self.booking.pk).complete)

        # Mark incomplete
        response = self.client.get(reverse('booking-incomplete', kwargs={'pk': self.booking.pk}))
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Booking.objects.get(pk=self.booking.pk).complete)
