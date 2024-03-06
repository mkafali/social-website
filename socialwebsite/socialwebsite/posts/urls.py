from django.urls import path
from . import views

urlpatterns = [
    path('create_post/', views.crate_post, name='create_post'),
    path('edit_post/<str:username>/<slug:post_slug>/', views.edit_post, name='edit_post'),
    path('delete_post/<str:username>/<slug:post_slug>/', views.delete_post, name='delete_post'),
    path('post/<str:username>/<slug:post_slug>/', views.post_pages, name='post_pages'),
    path('complain_post/<str:username>/<slug:post_slug>/', views.complain_post, name='complain_post'),
    path('like/<str:post_user>/<slug:post_slug>/', views.like_post, name='like_post'),
    path('who_liked/<str:post_user>/<slug:post_slug>/', views.who_liked, name='who_liked'),
    path('comment/<str:post_user>/<slug:post_slug>/', views.comment_post, name='comment'),
    path('comments/<str:post_user>/<slug:post_slug>/', views.who_comment_what, name='who_comment_what'),
    path('delete_comment/<slug:post_slug>/<str:commented_by>/<str:comment_slug>/', views.delete_comment, name='delete_comment'),
    path('comment_page/<slug:post_slug>/<str:commented_by>/<str:comment_slug>/', views.comment_page, name='comment_page'),
    path('complain_comment/<slug:post_slug>/<str:commented_by>/<str:comment_slug>/', views.complain_comment, name='complain_comment'),
    

]

