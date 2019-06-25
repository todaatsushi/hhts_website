from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, FormView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import EmailMessage


from .models import EmailBlast
from .forms import DraftEmailForm
from .helper import validate_emails


class AllBlastsView(LoginRequiredMixin, ListView):
    model = EmailBlast
    template_name = 'email_blast/index.html'
    context_object_name = 'emails'
    paginate_by = 5


class DraftMailView(LoginRequiredMixin, FormView):
    template_name = 'email_blast/draft_email.html'
    form_class = DraftEmailForm
    success_url = '/email/'

    def form_valid(self, form):
        form.save_draft(request=self.request)
        return super().form_valid(form)


class UpdateMailView(LoginRequiredMixin, UpdateView):
    model = EmailBlast
    template_name = 'email_blast/update_email.html'
    fields = ['recipients', 'subject', 'content', 'is_admin']
    success_url = '/email/'

    def form_valid(self, form):
        email = form.save(commit=False)
        email.last_updated_at = timezone.now()

        to = email.recipients
        validate_emails(to)
        to = to.split(',')

        if email.is_admin:
            admins = User.objects.all()
            admin_emails = map(lambda user: user.email, admins)
            admin_emails = list(admin_emails)

            for address in to:
                if address not in admin_emails:
                    raise ValidationError(
                        f'{address} is not an admin email!',
                        code='invalid'
                    )
        return super().form_valid(form)


class DeleteMailView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = EmailBlast
    template_name = 'email_blast/delete_mail.html'
    success_url = '/email/'

    def test_func(self):
        email = self.get_object()
        return email.sent == False


class ViewMailView(LoginRequiredMixin, DetailView):
    model = EmailBlast
    template_name = 'email_blast/view_send.html'
    context_object_name = 'email'


@login_required
def send_mail(request, pk):
    details = get_object_or_404(EmailBlast, pk=pk)
    print(details)
    email = EmailMessage(
        subject=details.subject,
        body=details.content,
        bcc=details.recipients.split(',')
    )

    email.send()
    details.mark_sent()
    details.save()
    messages.success(request, 'Sent Email')

    return HttpResponseRedirect(reverse('email-index'))
