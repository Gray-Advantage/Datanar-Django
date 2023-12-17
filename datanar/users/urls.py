from allauth.account.views import ConfirmEmailView
from allauth.account.views import EmailVerificationSentView
from allauth.account.views import EmailView
from allauth.account.views import LoginView
from allauth.account.views import LogoutView
from allauth.account.views import PasswordChangeView
from allauth.account.views import PasswordResetDoneView
from allauth.account.views import PasswordResetFromKeyDoneView
from allauth.account.views import PasswordResetFromKeyView
from allauth.account.views import PasswordResetView
from allauth.account.views import SignupView
from django.urls import path, re_path, reverse_lazy

from users import forms
from users import views


app_name = "users"

urlpatterns = [
    path(
        "account/",
        views.AccountView.as_view(),
        name="profile",
    ),
    path(
        "singup/",
        SignupView.as_view(
            form_class=forms.DatanarSignupForm,
            template_name="users/signup.html",
        ),
        name="signup",
    ),
    path(
        "login/",
        LoginView.as_view(
            form_class=forms.DatanarLoginForm,
            template_name="users/login.html",
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path(
        "confirm-email/",
        EmailVerificationSentView.as_view(
            template_name="users/confirm_email.html",
        ),
        name="confirm_email",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(
            template_name="users/confirm_email_from_sent.html",
        ),
        name="account_confirm_email",
    ),
    path(
        "email/",
        EmailView.as_view(
            form_class=forms.DatanarEmailForm,
            template_name="users/email_change.html",
        ),
        name="email_change",
    ),
    path(
        "password/change/",
        PasswordChangeView.as_view(
            form_class=forms.DatanarChangePasswordForm,
            template_name="users/password_change.html",
            success_url=reverse_lazy("users:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password/change/done/",
        views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path(
        "password/reset/",
        PasswordResetView.as_view(
            form_class=forms.DatanarResetPasswordForm,
            template_name="users/password_reset.html",
        ),
        name="password_reset",
    ),
    path(
        "password/reset/done/",
        PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        PasswordResetFromKeyView.as_view(
            form_class=forms.DatanarResetPasswordKeyForm,
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/key/done/",
        PasswordResetFromKeyDoneView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
