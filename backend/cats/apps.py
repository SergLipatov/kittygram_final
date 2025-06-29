"""Django application configuration for the cats module."""
from django.apps import AppConfig


class CatsConfig(AppConfig):
    """Configuration class for the cats Django application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cats'
