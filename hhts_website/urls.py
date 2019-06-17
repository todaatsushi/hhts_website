from django.contrib import admin
from django.contrib.auth import views as av
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import hhts_website.views as v
from users import views as uv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.home, name='home'),
    path('about/', v.about, name='about'),
    path('guide/', v.guide_info, name='guide'),
    path('saijo-tours/', v.saijo_info, name='saijo'),

    # User views
    path('users/', include('users.urls')),

    # Blog views
    path('blog/', include('blog.urls')),

    # Email blast views
    path('email/', include('email_blast.urls')),

    # Booking views
    path('booking/', include('booking.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
