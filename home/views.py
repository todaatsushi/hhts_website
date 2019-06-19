from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.http import Http404, HttpResponse
from django.utils.translation import gettext as _
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
    # make sure language is available
    valid = False
    for l in settings.LANGUAGES:
        if l[0] == language:
            valid = True
    if not valid:
        raise Http404(_('選択した言語は利用できません'))

    # Make language the setting for the session
    translation.activate(language)
    response = redirect(reverse('home'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response
