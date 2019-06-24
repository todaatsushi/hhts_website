from django.test import TestCase

from email_blast.forms import DraftEmailForm

import email_blast.helper as eh
import email_blast.tests.helper as h


class DraftEmailFormTestCase(TestCase):

    def setUp(self):
        self.user = h.create_user()

    def test_can_validate_valid_info(self):
        data = {
            'staff_recipients': [],
            'all_staff': False,
            'other_recipients': 'test@mail.com,\r\ntest2@mail.com',
            'subject': 'Test',
            'content': 'Test',
            'admin_email': False
        }

        form = DraftEmailForm(data)
        self.assertTrue(form.is_valid())

    def test_can_reject_invalid_info(self):
        data = {
            'staff_recipients': 'INVALID DATA',
            'all_staff': False,
            'other_recipients': 'test@mail.com,\r\ntest2@mail.com',
            'subject': 'Test',
            'content': 'Test',
            'admin_email': False
        }

        form = DraftEmailForm(data)
        self.assertFalse(form.is_valid())
