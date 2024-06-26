from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    LogoutView
)
from django.urls import path, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from . import views

app_name = 'users'
urlpatterns = [
    path(_('login/'), views.UserLoginView.as_view(), name='login'),
    path(_('logout/'), LogoutView.as_view(next_page=reverse_lazy('base:main')), name='logout'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path(_('registrationConfirmed/'),
         TemplateView.as_view(template_name='users/registration/reg_confirmed.html'),
         name='registrationConfirmed'),
    path(_('profile/'), views.Profile.as_view(), name='profile'),
    path(_('register/'), views.UserRegistration.as_view(), name="register"),
    path(_('passwordChange/'), views.ChangePasswordView.as_view(), name="password_change"),
    path(_('passwordChangeDone/'),
         PasswordChangeDoneView.as_view(template_name='users/registration/password_change_done.html'),
         name="password_change_done"
         ),

    path(_('passwordReset'),
         PasswordResetView.as_view(
             template_name='users/registration/password_reset_form.html',
             email_template_name='users/registration/password_reset_email.html',
             success_url=reverse_lazy('users:password_reset_done')
         ),
         name='password_reset'),
    path(
        _('passwordResetDone'),
        PasswordResetView.as_view(template_name='users/registration/password_reset_done.html'),
        name='password_reset_done'),
    path('passwordResetConfirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/registration/password_reset_confirm_form.html',
             success_url=reverse_lazy('users:password_reset_complete')
         ),
         name='password_reset_confirm'
         ),
    path('passwordResetComplete',
         PasswordResetCompleteView.as_view(
             template_name='users/registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
