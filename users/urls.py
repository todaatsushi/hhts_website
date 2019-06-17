from django.contrib import admin
from django.contrib.auth import views as av
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import hhts_website.views as v
from users import views as uv

urlpatterns = [   
     # User views
    path('register/', uv.register, name='user-reg'),
    path('team/', uv.TeamView.as_view(), name='team'),
    path('profile/<str:username>/', uv.user_profile, name='user-about'),
    path('profile/', uv.profile, name='user-profile'),

    # Authentication views
    path('login/', av.LoginView.as_view(template_name='users/login.html'), name='user-login'),
    path('logout/', av.LogoutView.as_view(template_name='users/logout.html'), name='user-logout'),
    path('password-reset/', av.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', av.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', av.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete', av.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]