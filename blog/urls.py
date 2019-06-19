from django.urls import path

import blog.views as v

urlpatterns = [
    path('', v.PublicPostView.as_view(), name='blog-home'),
    path('post/<int:pk>/', v.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', v.PostCreateView.as_view(), name='post-new'),
    path('post/admin_posts/', v.AdminPostView.as_view(), name='post-admin'),
    path('post/all/', v.BlogAllView.as_view(), name='post-all'),
    path('post/<str:username>/', v.AllUserPostView.as_view(), name='post-user'),
    path('post/<int:pk>/update/', v.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', v.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/pin/', v.pin_post, name='post-pin'),
    path('post/<int:pk>/unpin/', v.unpin_post, name='post-unpin'),
    path('post/<int:pk>/admin/', v.change_to_admin_post, name='post-admin'),
    path('post/<int:pk>/unadmin/', v.change_from_admin_post, name='post-unadmin'),
    path('post/<int:pk>/comment/', v.add_comment_to_post, name='post-comment'),
    path('post/<int:pk>/comment/<int:pkc>/delete/', v.comment_delete, name='post-comment_delete'),
    path('post/<int:pk>/comment/<int:pkc>/admin/', v.comment_admin, name='post-comment_admin'),
    path('post/<int:pk>/comment/<int:pkc>/unadmin/', v.comment_unadmin, name='post-comment_unadmin'),
]
