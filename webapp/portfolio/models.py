"""Database models for the portfolio application."""

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.gis.db import models
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from phonenumber_field.modelfields import PhoneNumberField

from webapp.portfolio.managers import CustomUserManager
from webapp.portfolio.validators import phone_number_validator


class Reference(models.Model):
    """Generate references for other models."""

    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "reference"
        verbose_name_plural = "references"

    @classmethod
    def generate_reference(cls, prefix: str) -> str:
        """Generate a unique reference number."""

        instance = cls.objects.create()
        suffix = f"{instance.pk}".zfill(6)
        return f"{prefix}-{suffix}"

    @classmethod
    def generate_username(cls) -> str:
        """Generate a unique reference number."""

        return cls.generate_reference(prefix="user")


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Models system user."""

    username = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(
        unique=True,
        error_messages={"unique": "A user with that email address already exists."},
        max_length=50,
        null=True,
        blank=True,
    )
    home_address = models.TextField(null=True, blank=True)
    location = models.PointField(default=None, blank=True, null=True)
    phone_number = PhoneNumberField(
        unique=True,
        error_messages={"unique": "A user with that phone number already exists."},
        max_length=50,
        null=True,
        blank=True,
        validators=[phone_number_validator],
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Designates whether this user should be treated as active."
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []  # type: ignore

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        default_manager_name = "objects"

    def __str__(self) -> str:
        """Return the username."""

        return self.username

    def clean(self) -> None:
        """Normalise the provided email."""

        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def url_safe_b64_encoded_id(self) -> str:
        """Encode the user id as a b64 url safe string."""

        return urlsafe_base64_encode(force_bytes(self.pk))

    def get_full_name(self) -> str:
        """Return the user first and last name as a single str."""

        names = [self.first_name, self.last_name]
        return " ".join(name for name in names if name)

    def get_short_name(self) -> str:
        """Return the short name for standard user model compatibility."""

        return self.first_name


class UserActivity(models.Model):
    """User login and logout activity model."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login = models.DateTimeField(auto_now_add=True)
    logout = models.DateTimeField(null=True, default=None)

    class Meta:
        verbose_name = "user activity"
        verbose_name_plural = "user activities"
        default_manager_name = "objects"

    def __str__(self) -> str:
        """Return the username."""

        return self.user.username
