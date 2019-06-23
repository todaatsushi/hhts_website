from django.utils import timezone

import os
import datetime

from booking.models import Booking


def create_booking():
    """
    Returns test Booking obj.
    """
    return Booking.objects.create(
        contact_name='Me',
        is_group=True,
        group_name='Fast 5',
        group_number=10,
        contact_number=12345,
        contact_address='Rio',
        contact_email=os.environ.get('GMAIL_ADDRESS'),
        scheduled_at=timezone.now().strftime('%Y-%m-%d %H:%M'),
        duration='60',
        age_group='ミックス',
        places_to_visit='All of them',
        transportation='自動車・バン',
        extra_details=None,
        booked_at=timezone.now().strftime('%Y-%m-%d %H:%M')
    )


def basic_view_check(test_case_obj, path, template, login_required,
                        login_desired, text_on_page):
    """
    Checks if view bounces non logged in user (or not) and the right template.

    Inputs:
        test_case_obj - 'self' in tests.
        path - reverse(x) or absolute url.
        template - app/template.html
        login_required - bool (If you need to be logged in to access)
        login_desired  - bool (If you want to test logged in vs logged out outputs)
        text_on_page - list of strings with contained texts.
                     - to assertNotContains, start the string with *!.

    Requires test case to have following properties:
        - test_case_obj.user: django.contrib.auth.models.User instance
    """

    # Checking authentication
    if login_required:
        not_logged_in_response = test_case_obj.client.get(path)
        test_case_obj.assertEqual(not_logged_in_response.status_code, 302) # Fail here - login auth is failing and/or not bouncing user to login page

    
    # If test is for logged out users trying to see logged in only content, exit test
    # i.e. login_desired is False and login_required is True
    if not login_desired and login_required:
        return

    if login_desired:
        test_case_obj.client.force_login(test_case_obj.user)

    # Checking templates used
    response = test_case_obj.client.get(path)
    test_case_obj.assertEqual(response.status_code, 200) # Fail here - didn't get a proper response
    test_case_obj.assertTemplateUsed(response, template) # Fail here - wrong template

    # Checking for text in the page
    for t in text_on_page:
        if t[0:2] == '*!':
            t = t[2:len(t)]
            test_case_obj.assertNotContains(response, t[2:len(t)]) # Fail here - template has string that shouldn't be there
        else:
            test_case_obj.assertContains(response, t) # Fail here - template doesn't have string that should be there
