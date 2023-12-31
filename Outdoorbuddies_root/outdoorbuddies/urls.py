from django.urls import path
from .views import register, about, contact, create_adventure, adventure_detail, profile
from .views import join_adventure, delete_adventure, search_results, user_profile
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path("", views.index, name="index"),
    path("register/", register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='outdoorbuddies/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='outdoorbuddies/logout.html'), name='logout'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('create-adevnture/', create_adventure, name='create_adventure'),
    path('liked-adventures/', views.liked_adventures, name='liked_adventures'),
    path('like-adventure/<int:adventure_id>/', views.like_adventure, name='like_adventure'),
    path('adventures/<int:adventure_id>/', adventure_detail, name='adventure_detail'),
    path('profile/', profile, name='profile'),
    path('user/<str:username>/', user_profile, name='user_profile'),
    path('search/', search_results, name='search_results'),
    path('join-adventure/<int:adventure_id>/', join_adventure, name='join_adventure'),
    path('delete-adventure/<int:adventure_id>/', delete_adventure, name='delete_adventure'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='outdoorbuddies/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='outdoorbuddies/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='outdoorbuddies/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='outdoorbuddies/password_reset_complete.html'), name='password_reset_complete'),
]