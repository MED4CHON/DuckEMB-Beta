"""
Application/apps.py

Es un registro de aplicaciones instaladas que almacena la configuración y proporciona introspección.
También mantiene una lista de modelos disponibles.

Para obtener más información sobre este archivo, consulte:
https://docs.djangoproject.com/en/4.1/ref/applications/
"""

from django.apps import AppConfig


class ApplicationConfig(AppConfig):
    """Esta es una clase de configuración de aplicación de Django que se utiliza para configurar y personalizar
        el comportamiento de la aplicación 'Application'.

    Args:
        AppConfig (class): Proporciona una manera de personalizar y configurar el comportamiento de la aplicación Django
        al permitir la definición de diferentes atributos y métodos dentro de una clase de configuración de la aplicación.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Application'
