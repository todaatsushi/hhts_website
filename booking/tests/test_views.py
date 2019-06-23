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

    def basic_view_check(self, path, template, login_required,
                         text_on_page):
        """
        Checks if view bounces non logged in user (or not) and the right template.

        Inputs:
            path - reverse(x) or absolute url.
            template - app/template.html
            login_required - bool
            text_on_page - list of strings with contained texts
        """

        # Helper func
        def check_auth(self, path):
            """
            Bounces non logged in sessions.
            """
            response = self.client.get(path)
            self.assertEqual(response.status_code, 302)


        if login_required:
            check_auth(self, path)
            self.client.force_login(self.user)

        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)

        for t in text_on_page:
            self.assertContains(response, t)

    def test_all_bookings_view(self):
        self.basic_view_check(
            path=reverse('booking-index'),
            template='booking/index.html',
            login_required=True,
            text_on_page=[
                '全てのブッキング', # Japanese text
                'Me', # Booking itself
            ]
        )

    def test_all_bookings_view_en(self):
        with self.english_setting():
            self.basic_view_check(
                reverse('booking-index'),
                'booking/index.html',
                True,
                [
                    'All bookings', # Japanese text
                    'Me', # Booking itself
                ]
            )

    def test_book_tour_create_view(self):
        self.basic_view_check(
            reverse('booking-book'),
            'booking/book_tour.html',
            True,
            [
                'ツアーを予約', # Japanese text
                '基本情報' # form in japanese
            ]
        )

    def test_book_tour_create_view_en(self):
        with self.english_setting():
            self.basic_view_check(
                reverse('booking-book'),
                'booking/book_tour.html',
                True,
                [
                    'Book a tour', # English text
                    'Basic information' # form in english
                ]
            )
    
    def test_booking_detail_view(self):
        self.basic_view_check(
            reverse('booking-detail', kwargs={'pk': self.booking.pk}),
            'booking/booking_view.html',
            True,
            [
                self.booking.contact_name,
                '連絡先' # Subtitle
            ]
        )

    def test_booking_detail_view_en(self):
        with self.english_setting():
            self.basic_view_check(
                reverse('booking-detail', kwargs={'pk': self.booking.pk}),
                'booking/booking_view.html',
                True,
                [
                    self.booking.contact_name,
                    'Contact information'
                ]
            )

    def test_booking_update_view(self):
        self.basic_view_check(
            reverse('booking-update', kwargs={'pk': self.booking.pk}),
            'booking/update.html',
            True,
            [
                'ツア更新',
                '予定時間' # Subtitle
            ]
        )

    def test_booking_update_view_en(self):
        with self.english_setting():
            self.basic_view_check(
                reverse('booking-update', kwargs={'pk': self.booking.pk}),
                'booking/update.html',
                True,
                [
                    'Update booking',
                    'Booking time' # Subtitle
                ]
            )

    def test_booking_delete_view(self):
        self.basic_view_check(
            reverse('booking-delete', kwargs={'pk': self.booking.pk}),
            'booking/confirm_delete.html',
            True,
            [
                'ツアのカンセル',
                '確認' # Confirm button text
            ]
        )

    def test_booking_delete_view_en(self):
        with self.english_setting():
            self.basic_view_check(
                reverse('booking-delete', kwargs={'pk': self.booking.pk}),
                'booking/confirm_delete.html',
                True,
                [
                    'Cancel tour',
                    'Confirm' # Confirm button text
                ]
            )

    def test_booking_confirm_view(self):
        with self.settings(
            EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
        ):
            self.client.force_login(self.user)
            self.assertFalse(self.booking.confirmed)
            response = self.client.get(reverse('booking-confirm', kwargs={'pk': self.booking.pk}))
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
