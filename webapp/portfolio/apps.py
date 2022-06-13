"""Expose the portfolio application configuration."""

from typing import Any

from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    """Django portfolio application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "webapp.portfolio"

    def ready(self) -> Any:
        """Signal."""

        import webapp.portfolio.signals  # noqa
