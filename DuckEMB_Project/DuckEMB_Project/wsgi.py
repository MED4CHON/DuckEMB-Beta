"""
DuckEMB_Project/wsgi.py

Configuración WSGI para el proyecto DuckEMB_Project.

Actúa como punto de entrada para la interfaz de servidor web de puerta de enlace de interfaz de servidor web
(Web Server Gateway Interface, WSGI). Esta es una especificación que define una interfaz estándar entre los
servidores web y las aplicaciones web escritas en Python, lo que permite que las aplicaciones web se ejecuten
en diferentes servidores web.

Este se utiliza para configurar la aplicación Django para ser servida en un servidor web compatible con WSGI,
como Apache o Nginx. En este archivo se encuentra la configuración para importar la aplicación de Django, inicializar
la configuración de la aplicación y crear un objeto WSGI que se encargará de manejar las solicitudes entrantes y las
respuestas salientes.

Expone el WSGI invocable como una variable de nivel de módulo llamada ``application``.

Para obtener más información sobre este archivo, consulte:
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DuckEMB_Project.settings')

application = get_wsgi_application()
