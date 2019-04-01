from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import Post, Comment
from .forms import CommentPostForm, CommentDeleteForm


class PublicPostView(ListView):
    model = Post
    template_name = 'blog/public_posts.html'
    context_object_name = 'posts'
    ordering = ['-pinned', '-posted_at']
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(admin_post=False).order_by('-pinned', '-posted_at')


class BlogAllView(ListView):
    model = Post
    template_name = 'blog/blog_all.html'
    context_object_name = 'posts'
    ordering = ['-pinned', '-posted_at']
    paginate_by = 5


class AllUserPostView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-pinned', '-posted_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context


class AdminPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/admin_posts.html'
    context_object_name = 'posts'
    ordering = ['-pinned', '-posted_at']
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(admin_post=True).order_by('-pinned', '-posted_at')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ['title', 'content', 'admin_post']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/update.html'
    fields = ['title', 'content', 'admin_post']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_at = timezone.now()
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


@login_required
def pin_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.pin()
    return HttpResponseRedirect(reverse('post-all'))


@login_required
def unpin_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.unpin()
    return HttpResponseRedirect(reverse('post-all'))


@login_required
def change_to_admin_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.admin()
    return HttpResponseRedirect(reverse('post-all'))


@login_required
def change_from_admin_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.unadmin()
    return HttpResponseRedirect(reverse('post-all'))


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentPostForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))
    else:
        form = CommentPostForm()

    context = {
        'form': form,
        'post': post
    }

    return render(request, 'blog/comment.html', context)


@login_required
def comment_delete(request, pk, pkc):
    comment = get_object_or_404(Comment, pk=pkc)

    if request.method == 'POST':
        form = CommentDeleteForm(request.POST)
        comment.delete()
        return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))
    else:
        form = CommentDeleteForm()

    context = {
        'form': form,
        'post': comment.post
    }

    return render(request, 'blog/delete_comment.html', context)


@login_required
def comment_admin(request, pk, pkc):
    comment = get_object_or_404(Comment, pk=pkc)
    comment.admin()
    comment.save()
    return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))


@login_required
def comment_unadmin(request, pk, pkc):
    comment = get_object_or_404(Comment, pk=pkc)
    comment.unadmin()
    comment.save()
    return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))
