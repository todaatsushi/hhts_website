from django.test import TestCase, Client

from django.urls import reverse


class HomeViewsTestCase(TestCase):

    def english_setting(self):
        return self.settings(LANGUAGE_CODE='en')

    def setUp(self):
        client = Client()


    def test_home_view_is_served(self):
        response = self.client.get(reverse('home'))

        # Successful check
        self.assertEqual(response.status_code, 200)

        # Template check
        self.assertTemplateUsed(response, 'home/home.html')

        # Right text (Japanese)
        self.assertContains(response, 'ようこそ')


    def test_about_view_is_served(self):
        response = self.client.get(reverse('about'))

        # Successful check
        self.assertEqual(response.status_code, 200)

        # Template check
        self.assertTemplateUsed(response, 'home/about.html')

        # Right text (Japanese)
        self.assertContains(response, '東広島探訪講座')


    def test_guide_view_is_served(self):
        response = self.client.get(reverse('guide'))

        # Successful check
        self.assertEqual(response.status_code, 200)

        # Template check
        self.assertTemplateUsed(response, 'home/guide.html')

        # Right text (Japanese)
        self.assertContains(response, 'ガイド派遣')


    def test_saijo_view_is_served(self):
        response = self.client.get(reverse('saijo'))

        # Successful check
        self.assertEqual(response.status_code, 200)

        # Template check
        self.assertTemplateUsed(response, 'home/saijo.html')

        # Right text (Japanese)
        self.assertContains(response, '西条の観光')

    
    def test_home_view_translation_works(self):
        with self.english_setting():
            response = self.client.get(reverse('home'))

            # Successful check
            self.assertEqual(response.status_code, 200)

            # Template check
            self.assertTemplateUsed(response, 'home/home.html')

            # Right text
            self.assertContains(response, 'Higashi Hiroshima')

    
    def test_about_view_translation_works(self):
        with self.english_setting():
            response = self.client.get(reverse('about'))

            # Successful check
            self.assertEqual(response.status_code, 200)

            # Template check
            self.assertTemplateUsed(response, 'home/about.html')

            # Right text
            self.assertContains(response, 'Exploration Course')

    
    def test_guide_view_translation_works(self):
        with self.english_setting():
            response = self.client.get(reverse('guide'))

            # Successful check
            self.assertEqual(response.status_code, 200)

            # Template check
            self.assertTemplateUsed(response, 'home/guide.html')

            # Right text
            self.assertContains(response, 'Dispatch')

    
    def test_saijo_view_translation_works(self):
        with self.english_setting():
            response = self.client.get(reverse('saijo'))

            # Successful check
            self.assertEqual(response.status_code, 200)

            # Template check
            self.assertTemplateUsed(response, 'home/saijo.html')

            # Right text
            self.assertContains(response, 'Sightseeing')
