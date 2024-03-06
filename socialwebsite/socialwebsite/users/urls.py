from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.log_out, name='log_out'),
    path('profile/', views.user_profile, name='user_profile'),
    path('register/', views.user_register, name='user_register'),
    path('edit/', views.profile_edit, name='edit_profile'),
    path('user_edit', views.user_edit, name='user_edit'),
    path('password_change/', views.password_change, name='password_change'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('forgot_my_password/', views.forgot_my_password, name='forgot_my_password'),
    path('confirm_password_code/', views.confirm_password_code, name='confirm_password_code'),
    path('new_password/', views.new_password, name='new_password'),
    path('user/<str:username>', views.user_pages, name='user_pages'),
    path('search/', views.search_something,name='search_something'),
    path('complain_user/<str:profile_username>/', views.complain_user, name='complain_user'),
    path('have_problem/', views.have_problem, name='have_problem'),
    path('my_likes/',views.my_likes, name='my_likes'),
    path('my_comments/', views.my_comments, name='my_comments'),
    path('follow/<str:follow_username>/', views.follow, name='follow'),
    path('followers/<str:username>/', views.display_followers, name='followers'),
    path('follows/<str:username>/', views.display_follows, name='follows'),
    path('block/<str:username>/', views.block, name='block'),
    

    

    
    

]

