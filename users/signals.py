from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.conf import settings

import os

from users.models import Profile


# Automatically create profile when User instance is made.
# If post_save is made (user is made, create profile)
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Save new profile after creation
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# Delete unused profile pictures on delete and on update
@receiver(post_delete, sender=User)
@receiver(post_save, sender=Profile)
@receiver(post_delete, sender=Profile)
def delete_unused_image_files(sender, instance, **kwargs):
    # All images currently in use
    in_use = [
        profile.image.url.replace('/media/', f'{settings.MEDIA_ROOT}/') for profile in Profile.objects.all()
    ]

    # Image locations
    image_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pics')
    all_pics = [
        f'{image_dir}/{pic}' for pic in os.listdir(image_dir)
    ]

    not_needed = [path for path in all_pics if path not in in_use]
    for path in not_needed:
        if path:
            default_storage.delete(path)
