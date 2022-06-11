"""Contains the application template based views."""

from django.contrib.auth import logout as auth_logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView

from webapp.portfolio import messages
from webapp.portfolio.forms import CustomUserCreationForm


class SignUpView(generic.CreateView):
    """Portfolio signup view."""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
@require_http_methods(["POST"])
def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    """Log the requesting user out."""

    auth_logout(request)
    messages.success(request=request, message="You have been successfully logged out.")
    return HttpResponseRedirect(reverse("home"))


class LoginView(auth_views.LoginView):
    """Portfolio login view."""

    template_name = "registration/login.html"


class HomeView(TemplateView):
    """Portfolio home view."""

    template_name = "accounts/index.html"


sign_up_view = SignUpView.as_view()
login_view = LoginView.as_view()
home_view = HomeView.as_view()
