from django.urls import path

from .views import AllBlastsView, DraftMailView, DeleteMailView, UpdateMailView, ViewMailView, send_mail

urlpatterns =[
    path('', AllBlastsView.as_view(), name='email-index'),
    path('draft/', DraftMailView.as_view(), name='email-draft'),
    path('<int:pk>/update/', UpdateMailView.as_view(), name='email-update'),
    path('<int:pk>/delete/', DeleteMailView.as_view(), name='email-delete'),
    path('<int:pk>/view/', ViewMailView.as_view(), name='email-view'),
    path('<int:pk>/send/', send_mail, name='email-send'),
]
