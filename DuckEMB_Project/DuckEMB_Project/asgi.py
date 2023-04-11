"""
DuckEMB_Project/asgi.py

Configuración ASGI para el proyecto DuckEMB_Project.

Es un archivo que se utiliza para configurar el servidor ASGI (Asynchronous Server Gateway Interface).
ASGI es una especificación que permite que los servidores web en Python manejen conexiones asincrónicas,
lo que permite que Django maneje de manera eficiente las solicitudes de los clientes en tiempo real,
como WebSocket y EventSource.

Este archivo se utiliza para configurar el servidor ASGI, que se utiliza para manejar solicitudes de
tiempo real, conexiones de larga duración y otras operaciones asincrónicas.

Expone el ASGI invocable como una variable de nivel de módulo llamada ``application``.

Para obtener más información sobre este archivo, consulte:
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DuckEMB_Project.settings')

application = get_asgi_application()
