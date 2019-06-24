from django.test import TestCase

from email_blast.models import EmailBlast
import email_blast.tests.helper as h


class EmailBlastTestCase(TestCase):

    def setUp(self):
        self.user = h.create_user()
        self.public = h.create_public_email(self.user)
        self.staff = h.create_admin_only_email(self.user)

    def test_can_make_emailblast(self):
        self.assertIsInstance(self.public, EmailBlast)
        self.assertIsInstance(self.staff, EmailBlast)

        self.assertEqual(self.public.__str__(), self.public.subject)
        self.assertEqual(self.staff.__str__(), self.staff.subject)

        self.assertEqual(
            self.public.__repr__(),
            f'{self.public.subject}, from {self.public.sender} at {self.public.sent_at}'
        )
        self.assertEqual(
            self.staff.__repr__(),
            f'{self.staff.subject}, from {self.staff.sender} at {self.staff.sent_at}')

    def test_email_mark_admin(self):
        self.assertFalse(self.public.is_admin)

        self.public.mark_admin()
        self.assertTrue(EmailBlast.objects.get(pk=self.public.pk).is_admin)

    def test_email_unmark_admin(self):
        self.assertTrue(self.staff.is_admin)
        self.staff.unmark_admin()
        self.assertFalse(EmailBlast.objects.get(pk=self.staff.pk).is_admin)
