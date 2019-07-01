from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth

from booking.tests.helper import basic_view_check
import users.tests.helper as h

from users.models import Profile
from users.forms import ProfileUpdateForm


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = h.create_user()
        self.profile = self.user.profile

        data = {}

        # Populate profile with data
        data['name'] = 'Giselle'
        data['about'] = 'Important member of the team.'
        data['image'] = h.create_dummy_image('test.png')
        data['role'] = 'Arms expert'
        form = ProfileUpdateForm(instance=self.profile, data=data)
        form.save()

    def english_setting(self):
        return self.settings(LANGUAGE_CODE='en')

    def test_index_view(self):
        response = self.client.get(reverse('user-home'))
        self.assertEqual(response.status_code, 302)

    def test_register_view(self):
        basic_view_check(
            test_case_obj=self,
            path=reverse('user-register'),
            template='users/register.html',
            login_required=True,
            login_desired=True,
            text_on_page=[
                'ユーザー申し込み'
            ]
        )

    def test_register_view_en(self):
        with self.english_setting():
            basic_view_check(
                test_case_obj=self,
                path=reverse('user-register'),
                template='users/register.html',
                login_required=True,
                login_desired=True,
                text_on_page=[
                    'Create a new user'
                ]
            )

    def test_team_view(self):
        basic_view_check(
            self,
            reverse('team'),
            'users/team.html',
            False,
            False,
            [
                'Giselle'
            ]
        )

    def test_profile_view(self):
        basic_view_check(
            self,
            reverse('user-about', kwargs={'username': self.user.username}),
            'users/profile.html',
            False,
            False,
            [
                'について',
                'Giselle'
            ]
        )

    def test_profile_view_en(self):
        with self.english_setting():
            basic_view_check(
                self,
                reverse('user-about', kwargs={'username': self.user.username}),
                'users/profile.html',
                False,
                False,
                [
                    'About',
                    'Giselle'
                ]
            )

    def test_login_view(self):
        basic_view_check(
            self,
            reverse('user-login'),
            'users/login.html',
            False,
            False,
            [
                'ログイン'
            ]
        )

    def test_login_view_en(self):
        with self.english_setting():
            basic_view_check(
                self,
                reverse('user-login'),
                'users/login.html',
                False,
                False,
                [
                    'Login'
                ]
            )

    def test_logout_view(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('user-logout'))
        self.assertEqual(response.status_code, 200)

        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
