from django.apps import AppConfig


class MudrykConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mudryk'
    default_site = 'my_custom_admin_site'
    verbose_name = 'Маленький Мудрик'