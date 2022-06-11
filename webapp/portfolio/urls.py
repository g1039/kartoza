"""Expose the application url config."""

from django.urls import path

from webapp.portfolio.views import home_view, login_view, logout_view, sign_up_view

urlpatterns = [
    path("", home_view, name="home"),
    path("signup/", sign_up_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
