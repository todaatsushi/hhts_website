from django.contrib import admin
from django.contrib.auth import views as av
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # User views
    path('users/', include('users.urls')),

    # Blog views
    path('blog/', include('blog.urls')),

    # Email blast views
    path('email/', include('email_blast.urls')),

    # Booking views
    path('booking/', include('booking.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    prefix_default_language=False
)
