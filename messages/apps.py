from django.apps import AppConfig


class CustomMessagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messages'
    label = 'custom_messages'   # For the purpose of avoiding conflict with in-built message app