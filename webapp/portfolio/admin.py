"""Admin panel for the portfolio application."""

from django.contrib.auth import get_user_model
from django.contrib.gis import admin
from django.utils.translation import gettext_lazy as _

from webapp.portfolio.forms import CustomUserCreationForm

User = get_user_model()

FIELDSETS = (
    (None, {"fields": ("email", "phone_number", "password")}),
    (
        _("Personal info"),
        {
            "fields": (
                "username",
                "first_name",
                "last_name",
            )
        },
    ),
    (
        _("Address info"),
        {"fields": ("home_address", "location")},
    ),
    (
        _("Permissions"),
        {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        },
    ),
    (_("Important dates"), {"fields": ("last_login", "date_joined")}),
)

ADD_FIELDSETS = (
    (
        None,
        {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        },
    ),
)


@admin.register(User)
class CustomUser(admin.OSMGeoAdmin):
    """Custom admin for the custom user model."""

    add_form = CustomUserCreationForm
    fieldsets = FIELDSETS
    add_fieldsets = ADD_FIELDSETS
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
    )
    readonly_fields = ("username",)
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone_number",
    )
    ordering = ("-pk",)
