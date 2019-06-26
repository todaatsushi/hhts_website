from django.test import TestCase, Client
from django.urls import reverse

from booking.tests.helper import basic_view_check
import email_blast.tests.helper as h

from email_blast.models import EmailBlast


class EmailBlastViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = h.create_user()
        self.public = h.create_public_email(self.user)
        self.staff = h.create_admin_only_email(self.user)

    def english_settings(self):
        return self.settings(LANGUAGE_CODE='en')

    def test_all_blasts_view(self):
        basic_view_check(
            test_case_obj=self,
            path=reverse('email-index'),
            template='email_blast/index.html',
            login_required=True,
            login_desired=True,
            text_on_page=[
                '全てのメール',
                'Test email'
            ]
        )

    def test_all_blasts_view_en(self):
        with self.english_settings():
            basic_view_check(
                self,
                reverse('email-index'),
                'email_blast/index.html',
                True,
                True,
                [
                    'All emails',
                    'Test email'
                ]
            )

    def test_draft_mail_view(self):
        basic_view_check(
            self,
            reverse('email-draft'),
            'email_blast/draft_email.html',
            True,
            True,
            [
                'メールを書く',
                'ドラフト',
            ]
        )

    def test_draft_mail_view_en(self):
        with self.english_settings():
            basic_view_check(
                self,
                reverse('email-draft'),
                'email_blast/draft_email.html',
                True,
                True,
                [
                    'email',
                    'Draft',
                ]
            )

    def test_update_mail_view(self):
        basic_view_check(
            self,
            reverse('email-update', kwargs={'pk': self.public.pk}),
            'email_blast/update_email.html',
            True,
            True,
            [
                'メールの更新'
            ]
        )

    def test_update_mail_view_en(self):
        with self.english_settings():
            basic_view_check(
                self,
                reverse('email-update', kwargs={'pk': self.public.pk}),
                'email_blast/update_email.html',
                True,
                True,
                [
                    'Update email'
                ]
            )

    def test_delete_mail_view(self):
        basic_view_check(
            self,
            reverse('email-delete', kwargs={'pk': self.public.pk}),
            'email_blast/delete_mail.html',
            True,
            True,
            [
                'メールを削除する'
            ]
        )

    def test_delete_mail_view_en(self):
        with self.english_settings():
            basic_view_check(
                self,
                reverse('email-delete', kwargs={'pk': self.public.pk}),
                'email_blast/delete_mail.html',
                True,
                True,
                [
                    'Delete email'
                ]
            )

    def test_view_mail_view(self):
        basic_view_check(
            self,
            reverse('email-view', kwargs={'pk': self.public.pk}),
            'email_blast/view_send.html',
            True,
            True,
            [
                'メールを確認してください',
                'Test email',
            ]
        )

    def test_view_mail_view_en(self):
        with self.english_settings():
            basic_view_check(
                self,
                reverse('email-view', kwargs={'pk': self.public.pk}),
                'email_blast/view_send.html',
                True,
                True,
                [
                    'Confirm your email before sending',
                    'Test email',
                ]
            )

    def test_send_mail(self):
        with self.settings(
            EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
        ):  
            # Test authentication
            non_logged_in_response = self.client.get(
                reverse('email-send', kwargs={'pk': self.public.pk})
            )
            self.assertEqual(non_logged_in_response.status_code, 302)


            self.client.force_login(self.user)
            logged_in_response = self.client.get(
                reverse('email-send', kwargs={'pk': self.public.pk})
            )
            # Check terminal to see the if the email has been sent
            self.assertEqual(logged_in_response.status_code, 302)

            # Make sure email is mark sent
            self.assertTrue(EmailBlast.objects.get(pk=self.public.pk).sent)
