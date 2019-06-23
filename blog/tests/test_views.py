from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from blog.models import Post
import blog.tests.helper as h
from booking.tests.helper import basic_view_check


class BlogViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = h.create_user()
        self.post = h.create_post(self.user)
        self.admin_post = h.create_admin_post(self.user)
        self.comment = h.create_comment(self.post)

    def english_setting(self):
        return self.settings(LANGUAGE_CODE='en')

    def test_public_post_view(self):
        basic_view_check(
            test_case_obj=self,
            path=reverse('blog-home'),
            template='blog/public_posts.html',
            login_required=False,
            login_desired=True,
            text_on_page=[
                'ブロッグ',
                '*!Admin test post'
            ]
        )

    def test_public_post_view_en(self):
        with self.english_setting():
            basic_view_check(
                self,
                reverse('blog-home'),
                'blog/public_posts.html',
                False,
                True,
                [
                    'Blog',
                    '*!Admin test post'
                ]
            )

    def test_blog_user_post_view_logged_out(self):
        basic_view_check(
            self,
            reverse('post-user', kwargs={'username': self.user.username}),
            'blog/user_posts.html',
            False,
            False,
            [
                f'{self.user.profile.name} のポスト',
                '*!Admin test post'
            ]
        )

    def test_blog_user_post_view_logged_out_en(self):
        with self.english_setting():
            basic_view_check(
                self,
                reverse('post-user', kwargs={'username': self.user.username}),
                'blog/user_posts.html',
                False,
                False,
                [
                    f'{self.user.profile.name} All Posts',
                    '*!Admin test post'
                ]
            )

    def test_blog_user_post_view_logged_in(self):
        basic_view_check(
            self,
            reverse('post-user', kwargs={'username': self.user.username}),
            'blog/user_posts.html',
            False,
            True,
            [
                f'{self.user.profile.name} のポスト',
                'Admin test post'
            ]
        )

    def test_blog_user_post_view_logged_in_en(self):
        with self.english_setting():
            basic_view_check(
                self,
                reverse('post-user', kwargs={'username': self.user.username}),
                'blog/user_posts.html',
                False,
                True,
                [
                    f'{self.user.profile.name} All Posts',
                    'Admin test post'
                ]
            )

    def test_admin_post_view_forbidden(self):
        # No login
        response = self.client.get(reverse('post-admin'))

        # Should redirect to login view
        self.assertEqual(response.status_code, 302)

    def test_admin_posts_view_logged_in(self):
        basic_view_check(
            self,
            reverse('post-admin'),
            'blog/admin_posts.html',
            True,
            True,
            [
                'スタフ専用',
                'Admin test post'
            ]
        )

    def test_admin_posts_view_logged_in_en(self):
        with self.english_setting():
            basic_view_check(
                self,
                reverse('post-admin'),
                'blog/admin_posts.html',
                True,
                True,
                [
                    'Staff only posts',
                    'Admin test post'
                ]
            )

    def test_create_view(self):
        basic_view_check(
            self,
            reverse('post-new'),
            'blog/create.html',
            True,
            True,
            [
                'ポストを新しく作る',
            ]
        )

    def test_create_view_en(self):
        with self.english_setting():
            basic_view_check(
                self,
                reverse('post-new'),
                'blog/create.html',
                True,
                True,
                [
                    'Create',
                ]
            )

    def test_update_view(self):
        basic_view_check(
            self,
            reverse('post-update', kwargs={'pk': self.post.pk}),
            'blog/update.html',
            True,
            True,
            [   
                'ポストの更新',
            ]
        )

    def test_update_view_en(self):
        with self.english_setting():
            basic_view_check(
                self,
                reverse('post-update', kwargs={'pk': self.post.pk}),
                'blog/update.html',
                True,
                True,
                [   
                    'Update post',
                ]
            )

    def test_delete_view(self):
        basic_view_check(
            self,
            reverse('post-delete', kwargs={'pk': self.post.pk}),
            'blog/confirm_delete.html',
            True,
            True,
            [   
                'ポスト削除',
            ]
        )

    def test_delete_view_en(self):
        with self.english_setting():
            basic_view_check(
                self,
                reverse('post-delete', kwargs={'pk': self.post.pk}),
                'blog/confirm_delete.html',
                True,
                True,
                [   
                    'Delete post',
                ]
            )

    def test_post_comment(self):
        basic_view_check(
            self,
            reverse('post-comment', kwargs={'pk': self.post.pk}),
            'blog/comment.html',
            False,
            True,
            [   
                'コメントを残す',
            ]
        )

    def test_post_comment_en(self):
        with self.english_setting():
            basic_view_check(
                self,
                reverse('post-comment', kwargs={'pk': self.post.pk}),
                'blog/comment.html',
                False,
                True,
                [   
                    'Comment',
                ]
            )

    def test_post_comment_delete_view(self):
        basic_view_check(
            self,
            reverse('post-comment_delete', kwargs={'pk': self.post.pk, 'pkc': self.comment.pk}),
            'blog/delete_comment.html',
            True,
            True,
            [   
                'コメント',
            ]
        )

    def test_post_comment_delete_view(self):
        with self.english_setting():
            basic_view_check(
                self,
                reverse('post-comment_delete', kwargs={'pk': self.post.pk, 'pkc': self.comment.pk}),
                'blog/delete_comment.html',
                True,
                True,
                [   
                    'Delete',
                ]
            )
        
    def test_post_detail_view_logged_out_and_viewing_normal_post(self):
        basic_view_check(
            self,
            reverse('post-detail', kwargs={'pk': self.post.pk}),
            'blog/post.html',
            False,
            False,
            [
                'Test content',
                '更新', # Button text on the page
            ]
        )

    def test_post_detail_view_logged_out_and_viewing_normal_post_en(self):
        with self.english_setting():
            basic_view_check(
                self,
                reverse('post-detail', kwargs={'pk': self.post.pk}),
                'blog/post.html',
                False,
                False,
                [
                    'Test content',
                    'Update', # Button text on the page
                ]
            )

    def test_post_detail_view_logged_in_and_viewing_admin_post(self):
        basic_view_check(
            self,
            reverse('post-detail', kwargs={'pk': self.admin_post.pk}),
            'blog/post.html',
            True,
            True,
            [
                'Admin test post'
            ]
        )

    def test_post_detail_view_logged_out_and_viewing_admin_post(self):
        basic_view_check(
            self,
            reverse('post-detail', kwargs={'pk': self.admin_post.pk}),
            'None', # Should end in redirect so no template needed
            True,
            False,
            [] # Same as template
        )

    def test_post_detail_view_logged_in_and_viewing_normal_post(self):
        basic_view_check(
            self,
            reverse('post-detail', kwargs={'pk': self.post.pk}),
            'blog/post.html',
            False,
            True,
            [
                'Test content',
                '更新'
            ]
        )

    def test_post_detail_view_logged_in_and_viewing_normal_post_en(self):
        with self.english_setting():
            basic_view_check(
                self,
                reverse('post-detail', kwargs={'pk': self.post.pk}),
                'blog/post.html',
                False,
                True,
                [
                    'Test content',
                    'Update'
                ]
            )


