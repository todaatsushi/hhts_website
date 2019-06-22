from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from blog.models import Post
import blog.tests.helper as h


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
        response = self.client.get(reverse('blog-home'))

        # Successful check
        self.assertEqual(response.status_code, 200)

        # Template check
        self.assertTemplateUsed(response, 'blog/public_posts.html')

        # Right text (Japanese)
        self.assertContains(response, 'ブロッグ')

        # No admin posts
        self.assertNotContains(response, 'Admin test post')

    def test_public_post_view_en(self):
        with self.english_setting():
            response = self.client.get(reverse('blog-home'))

            # Successful check
            self.assertEqual(response.status_code, 200)

            # Template check
            self.assertTemplateUsed(response, 'blog/public_posts.html')

            # Right text (Japanese)
            self.assertContains(response, 'Blog')
            
            # No admin posts
            self.assertNotContains(response, 'Admin test post')

    def test_blog_user_post_view_logged_out(self):
        # Make sure admin post is hidden
        response = self.client.get(reverse('post-user', kwargs={'username': self.user.username}))

        # Successful check
        self.assertEqual(response.status_code, 200)

        # Template check
        self.assertTemplateUsed(response, 'blog/user_posts.html')

        # Right text (Japanese)
        self.assertContains(response, f'{self.user.profile.name} のポスト')

        # Ensure admin post is not shown
        self.assertNotContains(response, 'Admin test post')

    def test_blog_user_post_view_logged_out_en(self):
        with self.english_setting():
            # Make sure admin post is hidden

            response = self.client.get(reverse('post-user', kwargs={'username': self.user.username}))

            # Successful check
            self.assertEqual(response.status_code, 200)

            # Template check
            self.assertTemplateUsed(response, 'blog/user_posts.html')

            # Right text (English)
            self.assertContains(response, f'{self.user.profile.name} All Posts')

            # Ensure admin post is not shown
            self.assertNotContains(response, 'Admin test post')

    def test_blog_user_post_view_logged_in(self):
        # Login
        self.client.force_login(User.objects.first())

        # Make sure admin post is hidden
        response = self.client.get(reverse('post-user', kwargs={'username': self.user.username}))

        # Successful check
        self.assertEqual(response.status_code, 200)

        # Template check
        self.assertTemplateUsed(response, 'blog/user_posts.html')

        # Right text (Japanese)
        self.assertContains(response, f'{self.user.profile.name} のポスト')

        # Ensure admin post is not shown
        self.assertContains(response, 'Admin test post')

    def test_blog_user_post_view_logged_in_en(self):
        with self.english_setting():
            self.client.force_login(User.objects.first())
            # Make sure admin post is hidden
            # Make admin post

            response = self.client.get(reverse('post-user', kwargs={'username': self.user.username}))

            # Successful check
            self.assertEqual(response.status_code, 200)

            # Template check
            self.assertTemplateUsed(response, 'blog/user_posts.html')

            # Right text (English)
            self.assertContains(response, f'{self.user.profile.name} All Posts')

            # Ensure admin post is shown
            self.assertContains(response, 'Admin test post')

    def test_admin_post_view_forbidden(self):
        # No login
        response = self.client.get(reverse('post-admin'))

        # Should redirect to login view
        self.assertEqual(response.status_code, 302)

    def test_admin_post_view_logged_in(self):
        self.client.force_login(User.objects.first())
        response = self.client.get(reverse('post-admin'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'blog/admin_posts.html')

        # Right text (English)
        self.assertContains(response, 'スタフ専用')

        # Ensure admin post is shown
        self.assertContains(response, 'Admin test post')

    def test_admin_post_view_logged_in_en(self):
        self.client.force_login(User.objects.first())
        
        with self.english_setting():
            response = self.client.get(reverse('post-admin'))

            self.assertEqual(response.status_code, 200)

            self.assertTemplateUsed(response, 'blog/admin_posts.html')

            # Right text (English)
            self.assertContains(response, 'Staff only posts')

            # Ensure admin post is shown
            self.assertContains(response, 'Admin test post')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post.html')
        self.assertContains(response, 'Test content')
        
        # Test button text for japanese
        self.assertContains(response, '更新')

    def test_post_detail_view_en(self):
        with self.english_setting():
            response = self.client.get(reverse('post-detail', kwargs={'pk': 1}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'blog/post.html')
            self.assertContains(response, 'Test content')
            
            # Test button text for english
            self.assertContains(response, 'Update')

    def test_create_view(self):
        self.client.force_login(User.objects.first())
        response = self.client.get(reverse('post-new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/create.html')
        self.assertContains(response, 'ポストを新しく作る')

    def test_create_view_en(self):
        self.client.force_login(User.objects.first())
        with self.english_setting():
            response = self.client.get(reverse('post-new'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'blog/create.html')
            self.assertContains(response, 'Create')

    def test_update_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('post-update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/update.html')
        self.assertContains(response, '更新')

    def test_update_view_en(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('post-update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/update.html')
        self.assertContains(response, 'ポストの更新')

    def test_delete_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('post-delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/confirm_delete.html')
        self.assertContains(response, 'ポスト削除')

    def test_delete_view_en(self):
        with self.english_setting():
            self.client.force_login(self.user)
            response = self.client.get(reverse('post-delete', kwargs={'pk': 1}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'blog/confirm_delete.html')
            self.assertContains(response, 'Delete post')

    def test_post_comment(self):
        response = self.client.get(reverse('post-comment', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/comment.html')
        self.assertContains(response, 'コメントを残す')

    def test_post_comment_en(self):
        with self.english_setting():
            response = self.client.get(reverse('post-comment', kwargs={'pk': 1}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'blog/comment.html')
            self.assertContains(response, 'Comment')

    def test_post_comment_delete_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('post-comment_delete', kwargs={'pk': self.post.pk, 'pkc': self.comment.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/delete_comment.html')
        self.assertContains(response, 'コメント')

    def test_post_comment_delete_view(self):
        with self.english_setting():
            self.client.force_login(self.user)
            response = self.client.get(reverse('post-comment_delete', kwargs={'pk': self.post.pk, 'pkc': self.comment.pk}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'blog/delete_comment.html')
            self.assertContains(response, 'Delete')
