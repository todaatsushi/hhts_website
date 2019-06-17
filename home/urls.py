from django.urls import path

import home.views as v


urlpatterns = [
    path('', v.home, name='home'),
    path('about/', v.about, name='about'),
    path('guide/', v.guide_info, name='guide'),
    path('saijo-tours/', v.saijo_info, name='saijo'),
]