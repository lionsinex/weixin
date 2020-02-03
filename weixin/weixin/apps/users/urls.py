# -*- coding: UTF-8 -*-

from django.urls import path

from users import register_view

urlpatterns = [
    path("register", register_view.RegisterView.as_view()),
    # path("login", login_view.LoginView.as_view()),
    # path("forget_password", forget_password_view.ForgetPasswordView.as_view()),
    # path("change_password", change_password_view.ChangePasswordView.as_view()),
    #
    # path("authenticate", authenticate_view.authenticate),
    # path("refresh_token", authenticate_view.refresh_token),
]
