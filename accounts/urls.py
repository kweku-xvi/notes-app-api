from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register-user'),
    path('login/', views.user_login, name='user-login'),
    path('users/', views.get_all_users_view, name='users'),
    path('password-reset/', views.password_reset_view, name='reset_password'),
    path('password-reset-confirm/', views.password_reset_confirm_view, name='password_reset_confirm_view')
]