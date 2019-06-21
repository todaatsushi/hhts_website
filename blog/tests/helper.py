from django.contrib.auth.models import User

from blog.models import Comment, Post


def create_user():
    """
    Returns a newly created User object that has already been saved in the db.
    """
    return User.objects.create_superuser(
        username='Atsushi',
        email='test@email.com',
        password='tesTing321'
    )


def create_post(user):
    """
    Returns a newly created Post object that has already been saved in the db.
    """
    return Post.objects.create(
        title='Test post',
        content='Test content',
        author=user
    )


def create_admin_post(user):
    """
    Returns a newly created Post object that has already been saved in the db.
    Post is only available to admins.
    """
    return Post.objects.create(
            title='Admin test post',
            content='test',
            author=user,
            admin_post=True,
        )


def create_comment(post):
    """
    Returns a newly created Comment object that has already been saved in the db.
    """
    return Comment.objects.create(
        post=post,
        commenter='Commenter',
        comment='Test comment'
    )
