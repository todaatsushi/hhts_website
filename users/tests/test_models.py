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
            self.data = self.profile.__dict__
            self.data['name'] = 'Brian'
            self.data['about'] = 'Best driver in the Fast crew.'
            self.data['role'] = 'Driver'

    def create_image(self, name='test.png'):
        return h.create_dummy_image(name)

    def test_can_make_profile(self):
        # Also tests the signal which creates the profile
        self.assertIsInstance(self.profile, Profile)

        self.assertEqual(
            self.profile.__str__(),
            f'{self.profile.name} - {self.user.username}'
        )

    def test_old_images_are_deleted_on_profile_instance_delete(self):
        with self.testing_media():
            # https://stackoverflow.com/a/34276961
            img = self.create_image()
            self.data['image'] = img
            form = ProfileUpdateForm(instance=self.profile, data=self.data)
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

    def test_old_images_are_deleted_on_user_instance_delete(self):
        with self.testing_media():
            # https://stackoverflow.com/a/34276961
            img = self.create_image()
            self.data['image'] = img

            form = ProfileUpdateForm(instance=self.profile, data=self.data)
            self.assertTrue(form.is_valid())

            form.save()

            image_path = pathlib.Path(
                os.path.join(settings.MEDIA_ROOT, 'profile_pics/test.png')
            )

            self.assertTrue(image_path.is_file())

            User.objects.first().delete()

            if image_path.is_file():
                image_path.unlink()
                raise  AssertionError('File has not been deleted.')

    def test_old_images_are_deleted_on_profile_update(self):
        with self.testing_media():
            # https://stackoverflow.com/a/34276961
            img = self.create_image()
            img2 = self.create_image('testing2.png')
            self.data['image'] = img

            form = ProfileUpdateForm(instance=self.profile, data=self.data)
            self.assertTrue(form.is_valid())

            form.save()

            image_path = pathlib.Path(
                os.path.join(settings.MEDIA_ROOT, 'profile_pics/test.png')
            )

            self.assertTrue(image_path.is_file())

            # Update data and user profile with new image
            self.data['image'] = img2
            form = ProfileUpdateForm(instance=self.profile, data=self.data)
            self.assertTrue(form.is_valid())
            form.save()

            self.assertFalse(image_path.is_file()) # old image should be gone
