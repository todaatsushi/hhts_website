from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView, FormView)
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage

from .models import Booking
from .forms import BookTourForm


class AllBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking/index.html'
    context_object_name = 'bookings'
    paginate_by = 5


class BookTourView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = 'booking/book_tour.html'
    form_class = BookTourForm
    success_url = '/booking/'

    def form_valid(self, form):
        form.instance.booked_at = timezone.now()
        print(form.data)
        return super().form_valid(form)


class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'booking/booking_view.html'
    context_object_name = 'booking'


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    template_name = 'booking/update.html'
    fields = [
        'scheduled_at', 'duration', 'transportation', 'places_to_visit',
        'contact_name', 'contact_number', 'contact_email', 'contact_address',
        'is_group', 'group_name', 'group_number', 'age_group',
        'extra_details'
    ]
    success_url = '/booking/'

    def form_valid(self, form):
        form.instance.completed = False
        form.instance.confirmed = False
        form.instance.booked_at = timezone.now()
        return super().form_valid(form)



class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'booking/confirm_delete.html'
    success_url = '/booking/'


@login_required
def booking_confirm(request, pk):
    booking = get_object_or_404(Booking, id=pk)
    booking.confirm()
    return HttpResponseRedirect(reverse('booking-index'))


@login_required
def booking_unconfirm(request, pk):
    booking = get_object_or_404(Booking, id=pk)
    booking.unconfirm()
    return HttpResponseRedirect(reverse('booking-index'))


@login_required
def booking_complete(request, pk):
    booking = get_object_or_404(Booking, id=pk)
    booking.done()
    return HttpResponseRedirect(reverse('booking-index'))


@login_required
def booking_incomplete(request, pk):
    booking = get_object_or_404(Booking, id=pk)
    booking.not_done()
    return HttpResponseRedirect(reverse('booking-index'))
