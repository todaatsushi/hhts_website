from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.http import Http404, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.template.loader import render_to_string


def home(request):
    return render(request, 'home/home.html')


def about(request):
    return render(request, 'home/about.html')


def guide_info(request):
    return render(request, 'home/guide.html')


def saijo_info(request):
    return render(request, 'home/saijo.html')


def change_language(request, language):
    redirect_url_name = request.GET.get('url_name')

    # Split url path and find the slug
    url_components = request.GET.get('full_path').split('/')
    url_components = [part for part in url_components if part]
    
    # List of bools indicating which url_components are numerical slugs ie. pk
    detail_page = []

    for i in url_components:
        # If int, i is a pk so log. else i is either app indicator
        # or a username in the user app
        try:
            int(i)
            detail_page.append(True)
        except ValueError:
            detail_page.append(False)

    try:
        # Home page will raise an index error
        if url_components[0] == 'users':
            # If the url is users, add the username as the slug
            slug = {'username': url_components[2]}
        elif any(detail_page):
            # Else if there is an int, add that as the slug
            slug = {'pk': url_components[detail_page.index(True)]}
        else:
            # Otherwise there is no slug e.g. list view
            slug = None

        # make sure language is available
        valid = False
        for l in settings.LANGUAGES:
            if l[0] == language:
                valid = True
        if not valid:
            raise Http404(_('選択した言語は利用できません'))

    except IndexError:
        slug = None

    # Make language the setting for the session
    translation.activate(language)

    if slug:
        # Assign slug if valid
        response = redirect(reverse(redirect_url_name, kwargs=slug))
    else:
        response = redirect(reverse(redirect_url_name))

    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response
