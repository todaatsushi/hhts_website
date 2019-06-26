from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

import os
import pathlib

import users.tests.helper as h
from users.models import Profile
from users.forms import ProfileUpdateForm


class ProfileModelTestCase(TestCase):
    
    def testing_media(self):
        return self.settings(MEDIA_ROOT=os.path.join(settings.SITE_ROOT, 'test_media'))
    
    def setUp(self):
        with self.testing_media():
            self.user = h.create_user()
            self.profile = self.user.profile # Profile is created by signal

    def create_image(self, name='test.png'):
        return h.create_dummy_image(name)

    def test_can_make_profile(self):
        # Also tests the signal which creates the profile
        self.assertIsInstance(self.profile, Profile)

        self.assertEqual(
            self.profile.__str__(),
            f'{self.profile.name} - {self.user.username}'
        )

    def test_old_images_are_deleted_on_instance_delele(self):
        with self.testing_media():
            # https://stackoverflow.com/a/34276961
            img = self.create_image()
            data = {
                'image': img,
                'name': "Brian O'Conner",
                'about': 'One of the leaders of the team and a world class driver.',
                'role': 'Driver',
            }

            form = ProfileUpdateForm(instance=self.profile, data=data)
            self.assertTrue(form.is_valid())

            form.save()

            image_path = pathlib.Path(
                os.path.join(settings.MEDIA_ROOT, 'profile_pics/test.png')
            )

            self.assertTrue(image_path.is_file())

            Profile.objects.first().delete()

            if image_path.is_file():
                image_path.unlink()
                raise  AssertionError('File has not been deleted.')
