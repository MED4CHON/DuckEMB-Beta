"""
DuckEMB_Project/urls.py

Configuración de URL del proyecto 'DuckEMB_Project'.

Es un archivo que se utiliza para definir las rutas de URL para aplicaciones web (En este caso desde el proyecto).

Es un archivo que se encuentra dentro de cada aplicación de Django y se utiliza para mapear las solicitudes de URL entrantes
a las funciones de vista correspondientes que generan la respuesta adecuada.

Se pueden definir diferentes rutas de URL para una aplicación, especificando una URL de patrón y la
función de vista que se debe llamar cuando se recibe una solicitud para esa URL. El patrón de URL puede incluir
variables, que se pueden pasar como argumentos a la función de vista correspondiente.

La lista `urlpatterns` enruta las URL a las vistas.

Ejemplos:

    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')

    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

Para obtener más información sobre este archivo, consulte:
https://docs.djangoproject.com/en/4.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from Application.views import password_reset_request
from django.contrib.auth import views as auth_views

from django.conf.urls import handler400, handler403, handler404, handler500
from Application.views import Error400View, Error403View, Error404View, Error500View


urlpatterns = [
    path('admin/', admin.site.urls), # Para el panel de administración.
    path('', include('Application.urls')), # Para las direcciones incluidas en la app 'Application'.
    path('accounts/', include('django.contrib.auth.urls')),

    # URLs para la recuperación de contraseñas.
    path('change-password/',auth_views.PasswordChangeView.as_view(template_name='Password/change-password.html'),),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='Password/change-password-done.html'), name='password_change_done',),
    path('reset_password/', password_reset_request, name='password_reset'),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(template_name='Password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='Password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Password/password_reset_complete.html'), name='password_reset_complete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URLs de HTTP Errors.
handler400 = Error400View.as_view()
handler403 = Error403View.as_view()
handler404 = Error404View.as_view()
handler500 = Error500View.as_error_view()