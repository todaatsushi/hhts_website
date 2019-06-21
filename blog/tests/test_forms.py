from django.test import TestCase
from django.contrib.auth.models import User

from blog.forms import CommentPostForm, CommentDeleteForm
from blog.models import Comment, Post

import blog.tests.helper as h


class CommentFormTestCase(TestCase):

    def setUp(self):
        self.user = h.create_user()
        self.post = h.create_post(self.user)
        self.comment = h.create_comment(self.post)
        self.data = self.comment.__dict__

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
        form = CommentPostForm({
            'post': self.post,
            'commenter': 'Test user',
            'comment': 'Test comment'
        })
        
        comment = form.save(commit=False)
        comment.post = self.post
        comment.save()
        self.assertIsInstance(Comment.objects.last(), Comment)



class CommentDeleteFormTestCase(TestCase):

    def setUp(self):
        self.user = h.create_user()
        self.post = h.create_post(self.user)
        self.comment = h.create_comment(self.post)
        self.data = self.comment.__dict__

    def test_comment_delete_form_is_valid(self):
        self.data['confirm'] = True
        form = CommentDeleteForm(instance=self.comment, data=self.data)
        self.assertTrue(form.is_valid())
