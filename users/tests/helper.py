from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

from users.models import Profile

from PIL import Image
from io import BytesIO


def create_user():
    return User.objects.create(
        username='brianoconner',
        email='test@mail.com',
        password='testING321'
    )


def create_dummy_image(name):
    """
    Returns a newly created png format image file.
    """
    # New PIL Image
    image = Image.new(mode='RGB', size=(200,200))

    # BytesIO obj for saving the image
    image_io = BytesIO()

    # Save the image
    image.save(image_io, 'PNG')

    # Seek to start
    image_io.seek(0)

    return InMemoryUploadedFile(
        image_io, None, name, 'image/png', len(image_io.getvalue()), None
    )
