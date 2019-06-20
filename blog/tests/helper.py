from django.contrib.auth.models import User

from blog.models import Comment, Post


def create_comment():
    """
    Returns a newly created Comment object that has already been saved in the db.
    """
    me = User.objects.create(
        username='Atsushi',
        email='test@email.com',
        password='tesTing321'
    )

    post = Post.objects.create(
        title='Test post',
        content='Test content',
        author=me
    )
    return Comment.objects.create(
        post=post,
        commenter='Commenter',
        comment='Test comment'
    )
