"""Contains the application template based views."""

from typing import Any

from django.contrib.auth import logout as auth_logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from webapp.portfolio import messages, services
from webapp.portfolio.forms import CustomUserCreationForm, ProfileDetailsForm
from webapp.portfolio.mixins import ReadOnlyThemedFormMixin
from webapp.portfolio.parsers import parse_boolean


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


class ProfileDetailView(ReadOnlyThemedFormMixin, FormView):
    """Profile detail section."""

    template_name = "profile/profile.html"
    form_class = ProfileDetailsForm
    success_url = reverse_lazy("profile-detail")

    def get_is_editable(self) -> bool:
        """If True the form fields will be disabled."""

        return parse_boolean(self.request.GET.get("editable", False))

    def get_initial(self) -> Any:
        """Return the initial data to use for forms on this view."""

        return {
            "first_name": self.request.user.first_name,
            "last_name": self.request.user.last_name,
            "email": self.request.user.email,
            "home_address": self.request.user.home_address,
            "phone_number": self.request.user.phone_number,
        }

    def form_valid(self, form: ProfileDetailsForm) -> HttpResponseRedirect:
        """Update the user profile details."""

        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        home_address = form.cleaned_data["home_address"]
        phone_number = form.cleaned_data["phone_number"]

        services.update_profile_details(
            user=self.request.user,
            first_name=first_name,
            last_name=last_name,
            home_address=home_address,
            phone_number=phone_number,
        )

        messages.success(
            request=self.request,
            message="Profile details updated.",
            auto_close_after_ms=5000,
        )

        return super().form_valid(form=form)


sign_up_view = SignUpView.as_view()
login_view = LoginView.as_view()
home_view = HomeView.as_view()
profile_detail_view = ProfileDetailView.as_view()
