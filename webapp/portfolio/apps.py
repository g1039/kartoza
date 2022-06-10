"""Expose the portfolio application configuration."""

from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    """Django portfolio application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "webapp.portfolio"
