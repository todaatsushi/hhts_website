from django.urls import path

import booking.views as v


urlpatterns = [
    path('', v.AllBookingsView.as_view(), name='booking-index'),
    path('new/', v.BookTourView.as_view(), name='booking-book'),
    path('<int:pk>/', v.BookingDetailView.as_view(), name='booking-detail'),
    path('<int:pk>/update/', v.BookingUpdateView.as_view(), name='booking-update'),
    path('<int:pk>/delete/', v.BookingDeleteView.as_view(), name='booking-delete'),
    path('<int:pk>/confirm/', v.booking_confirm, name='booking-confirm'),
    path('<int:pk>/complete/', v.booking_complete, name='booking-complete'),
    path('<int:pk>/unconfirm/', v.booking_unconfirm, name='booking-unconfirm'),
    path('<int:pk>/incomplete/', v.booking_incomplete, name='booking-incomplete'),
]
