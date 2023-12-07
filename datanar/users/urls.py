from django.contrib.auth import views as dj_views
from django.urls import path

from users import forms
from users import views


app_name = "users"

urlpatterns = [
    path(
        "activate/<str:username>/",
        views.ActivateView.as_view(),
        name="activate",
    ),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "login/",
        dj_views.LoginView.as_view(
            form_class=forms.DatanarAuthenticationForm,
            template_name="users/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        dj_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path(
        "password_change/",
        dj_views.PasswordChangeView.as_view(
            form_class=forms.DatanarPasswordChangeForm,
            template_name="users/password_change.html",
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        dj_views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        dj_views.PasswordResetView.as_view(
            form_class=forms.DatanarPasswordResetForm,
            template_name="users/password_reset.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        dj_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        dj_views.PasswordResetConfirmView.as_view(
            form_class=forms.DatanarPasswordResetConfirmForm,
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        dj_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
