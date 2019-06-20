from django.test import TestCase
from django.contrib.auth.models import User

from blog.forms import CommentPostForm, CommentDeleteForm
from blog.models import Comment, Post

from blog.tests.helper import create_comment as cc


class CommentFormTestCase(TestCase):

    def setUp(self):
        self.comment = cc()
        self.data = self.comment.__dict__

    # def test_comment_admin_and_unadmin(self):
    #     self.assertFalse(self.comment.by_admin)
    #     self.comment.admin()

    #     self.assertTrue(self.comment.by_admin)
    #     self.comment.unadmin()
        
    #     self.assertFalse(self.comment.by_admin)

    def test_comment_post_form_can_validate_data(self):
        del self.data['_state']
        form = CommentPostForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_comment_post_form_can_detect_invalid_data(self):
        del self.data['_state']
        self.data['comment'] = None
        form = CommentPostForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_comment_post_form_can_create_comment(self):    
        me = User.objects.create(
            username='Atsushi2',
            email='test@email.com',
            password='tesTing321'
        )
        post = Post.objects.create(
            title='Test post',
            content='Test content',
            author=me
        )
        form = CommentPostForm({
            'post': post,
            'commenter': 'Test user',
            'comment': 'Test comment'
        })
        
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        self.assertIsInstance(Comment.objects.last(), Comment)



class CommentDeleteFormTestCase(TestCase):

    def setUp(self):
        self.comment = cc()
        self.data = self.comment.__dict__

    def test_comment_delete_form_is_valid(self):
        self.data['confirm'] = True
        form = CommentDeleteForm(instance=self.comment, data=self.data)
        self.assertTrue(form.is_valid())
