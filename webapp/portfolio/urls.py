"""Expose the application url config."""

from django.urls import path

from webapp.portfolio.views import (
    home_view,
    login_view,
    logout_view,
    markers_map_view,
    profile_detail_view,
    sign_up_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("signup/", sign_up_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_detail_view, name="profile-detail"),
    path("map/", markers_map_view, name="markers-map"),
]
