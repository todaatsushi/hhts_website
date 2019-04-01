from django.urls import path

from .views import (BlogAllView, PostDetailView, PostCreateView, AllUserPostView,
                    PostUpdateView, PostDeleteView, pin_post, unpin_post, AdminPostView,
                    change_to_admin_post, change_from_admin_post, add_comment_to_post,
                    comment_delete, comment_admin, comment_unadmin, PublicPostView)

urlpatterns = [
    path('', PublicPostView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-new'),
    path('post/admin_posts/', AdminPostView.as_view(), name='post-admin'),
    path('post/all/', BlogAllView.as_view(), name='post-all'),
    path('post/<str:username>/', AllUserPostView.as_view(), name='post-user'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/pin/', pin_post, name='post-pin'),
    path('post/<int:pk>/unpin/', unpin_post, name='post-unpin'),
    path('post/<int:pk>/admin/', change_to_admin_post, name='post-admin'),
    path('post/<int:pk>/unadmin/', change_from_admin_post, name='post-unadmin'),
    path('post/<int:pk>/comment/', add_comment_to_post, name='post-comment'),
    path('post/<int:pk>/comment/<int:pkc>/delete/', comment_delete, name='post-comment_delete'),
    path('post/<int:pk>/comment/<int:pkc>/admin/', comment_admin, name='post-comment_admin'),
    path('post/<int:pk>/comment/<int:pkc>/unadmin/', comment_unadmin, name='post-comment_unadmin'),
]
