from django.test import TestCase
# from django.contrib.auth.models import User

from blog.models import Post, Comment

import blog.tests.helper as h


class CommentTestCase(TestCase):

    def setUp(self):
        self.user = h.create_user()
        self.post = h.create_post(self.user)
        self.comment = h.create_comment(self.post)
        self.data = self.post.__dict__
    
    def test_can_make_post(self):
        self.assertIsInstance(self.comment, Comment)
        self.assertEqual(self.comment.__str__(), f"{self.comment.commenter}: {self.comment.comment}")

    def test_comment_admin_and_unadmin(self):
        self.assertFalse(self.comment.by_admin)
        self.comment.admin()

        self.assertTrue(self.comment.by_admin)
        self.comment.unadmin()
        
        self.assertFalse(self.comment.by_admin)


class PostTestCase(TestCase):
    
    def setUp(self):
        self.user = h.create_user()
        self.post = h.create_post(self.user)

    def test_can_make_post(self):
        self.assertIsInstance(self.post, Post)
        self.assertEqual(self.post.__str__(), self.post.title)
        self.assertEqual(self.post.__repr__(), f'{self.post.title} by {self.post.author}')

    def test_post_get_absolute_url(self):
        self.assertEqual(
            self.post.get_absolute_url(),
            '/blog/post/1/',
        )

    def test_post_pin_and_unpin(self):
        self.assertFalse(self.post.pinned)
        self.post.pin()
        self.assertTrue(self.post.pinned)
        self.post.unpin()
        self.assertFalse(self.post.pinned)

    def test_post_admin_and_unadmin(self):
        self.assertFalse(self.post.admin_post)
        self.post.admin()
        self.assertTrue(self.post.admin_post)
        self.post.unadmin()
        self.assertFalse(self.post.admin_post)
