from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


@login_required
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account made for {username}. Please login.')
            return HttpResponseRedirect(reverse('blog-home'))
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})



def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, f'Account {username} does not exist.')
        return HttpResponseRedirect(reverse('blog-home'))

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Account {username} has been updated.')
            return HttpResponseRedirect(reverse('user-about', kwargs={'username': user.username}))

    if request.user == user:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    else:
        user_form = None
        profile_form = None

    context = {
        'person': user,
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'users/profile.html', context)


@login_required
def profile(request):
    user = request.user
    return HttpResponseRedirect(reverse('user-about', kwargs={'username': user.username}))


class TeamView(ListView):
    model = User
    template_name = 'users/team.html'
    context_object_name = 'team'
    ordering = ['id']
    paginate_by = 5
