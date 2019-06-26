from django.test import TestCase

import users.forms as f
import users.tests.helper as h

class UserFormsTestCase(TestCase):
    def setUp(self):
        self.user = h.create_user()
        self.profile = self.user.profile
    
    def test_user_register_form_can_validate_valid_info(self):
        data = {
            'username': 'test_user',
            'email': 'test@mail.com',
            'password1': 'testiNG321',
            'password2': 'testiNG321'
        }

        form = f.UserRegisterForm(data)
        self.assertTrue(form.is_valid())

    def test_user_register_form_can_detect_invalid_info(self):
        data = {
            'username': None,
            'email': 'test@mail.com',
            'password1': 'testiNG321',
            'password2': 'testiNG321'
        }

        form = f.UserRegisterForm(data)
        self.assertFalse(form.is_valid())

    def test_user_update_form_can_validate_valid_info(self):
        data = {
            'username': 'test_user',
            'email': 'test@mail.com',
            'password1': 'testiNG321',
            'password2': 'testiNG321'
        }
        form = f.UserUpdateForm(instance=self.user, data=data)
        self.assertTrue(form.is_valid())
    
    def test_user_update_form_can_detect_invalid_data(self):
        data = {
            'username': None,
            'email': 'test@mail.com',
            'password1': 'testiNG321',
            'password2': 'testiNG321'
        }
        form = f.UserUpdateForm(instance=self.user, data=data)
        self.assertFalse(form.is_valid())

    def test_profile_update_form_can_detect_valid_info(self):
        data = {
            'image': h.create_dummy_image('test.png'),
            'name': 'Dom',
            'about': 'One of the leaders in the team.',
            'role': 'Driver'
        }
        form = f.ProfileUpdateForm(instance=self.user.profile, data=data)
        self.assertTrue(form.is_valid())
