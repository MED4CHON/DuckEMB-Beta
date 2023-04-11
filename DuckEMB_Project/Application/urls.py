"""
Application/urls.py

Configuración de URL de la aplicación 'Application'.

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

from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [path('', vHome, name='Home'),
               path('terminos/', views.terminos, name='Terminos y Condiciones'),
               path('ejemplo/', VistaEjemplo.as_view(), name='Ejemplo_Error_500'),

               # Section - Autentificación
               path('register/', views.registerPage, name="register"),
               path('login/', LoginView.as_view(template_name='login.html'), name="login"),
               path('logout/', LogoutView.as_view(template_name='logout.html'), name="logout"),

               # Section - Categorias
               path('categorias/', Categoria, name='Categorias'),
               path('newcategoria/', NewCategoriaView.as_view(), name='Nueva Categoria'),
               path('modcategoria/<int:pk>/', views.ModCategoriaView.as_view(), name='ModCategoria'),
               path('deletecategoria/<int:pk>/', DeleteCategoriaView.as_view(), name='Eliminar Categoria'),
               path('articulosxcategoria/<int:pk>/', views.ArticulosxCategoria, name='Detalle Articulos-Categoria'),

               # Section - Clientes
               path('clientes/', vClienteDireccion, name='Clientes'),
               path('newcliente/', views.CreateCliente.as_view(), name="Nuevo Cliente - Multiple"),
               path('modcliente/<int:pk>/', UpdateCliente.as_view(), name='Modificar Cliente Doble'),
               path('deletecliente/<int:pk>/', DeleteClienteView.as_view(), name='Eliminar Cliente'),
               path('pedidoxcliente/<int:pk>/', views.PedidoxCliente, name='Detalle Pedido-Cliente'),

               # Section - Proveedores
               path('proveedores/', vProveedorDireccion, name='Proveedores'),
               path('newproveedor/', views.CreateProveedor.as_view(), name="Nuevo Proveedor - Multiple"),
               path('modproveedor/<int:pk>/', UpdateProveedor.as_view(), name='Modificar Proveedor'),
               path('deleteproveedor/<int:pk>/', DeleteProveedorView.as_view(), name='Eliminar Proveedor'),
               path('adquisiciónxproveedor/<int:pk>/', views.AdquisiciónxProveedor, name='Detalle Adquisicion-Proveedor'),

               # Section - Empleados
               path('empleados/', vEmpleadoDireccion, name='Empleados'),
               path('newempleado/', views.CreateEmpleado.as_view(), name="Nuevo Empleado - Multiple"),
               path('modempleado/<int:pk>/', UpdateEmpleado.as_view(), name='Modificar Empleado'),
               path('deleteempleado/<int:pk>/', DeleteEmpleadoView.as_view(), name='Eliminar Empleado'),
               path('empleados/administrativo/', views.Empleado_AD, name='Empleados administrativos'),
               path('empleados/obrero/', views.Empleado_OB, name='Empleados'),
               path('empleados/temporario/', views.Empleado_TE, name='Empleados'),
               path('empleados/gerencia/', views.Empleado_GE, name='Empleados'),
               path('empleados/ventas/', views.Empleado_VE, name='Empleados'),
               path('empleados/logistica/', views.Empleado_LO, name='Empleados'),
               path('cajaxempleado/<int:pk>/', views.CajaxEmpleado, name='Detalle Caja-Empleado'),

               # Section - Obras
               path('obras/', vObraDireccion, name='Obras'),
               path('newobra/', views.CreateObra.as_view(), name="Nuevo Obra - Multiple"),
               path('modobra/<int:pk>/', UpdateObra.as_view(), name='Modificar Obra'),
               path('deleteobra/<int:pk>/', DeleteObraView.as_view(), name='Eliminar Obra'),

               # Section - Piscinas
               path('piscinas/', views.vPiscinas, name='Piscinas'),
               path('newpiscina/', views.NewPiscinaView.as_view(), name='Nueva Piscina'),
               path('modpiscina/<int:pk>/', ModPiscinaView.as_view(), name='Modificar Piscina'),
               path('deletepiscina/<int:pk>/', DeletePiscinaView.as_view(), name='Eliminar Piscina'),
               path('detailpiscina/<int:pk>/', views.DetailPiscina, name='Detail Piscinas'),
               path('adquisiciónxpiscinas/<int:pk>/', views.AdquisicionxPiscinas, name='Detalle Adquisicion-Piscinas'),
               path('pedidoxpiscinas/<int:pk>/', views.PedidoxPiscinas, name='Detalle Pedido-Piscinas'),

               # Section - Articulos
               path('articulos/', views.vArticulos, name='Articulos'),
               path('newarticulo/', views.NewArticuloView.as_view(), name='Nueva Articulo'),
               path('modarticulo/<int:pk>/', ModArticuloView.as_view(), name='Modificar Articulo'),
               path('deletearticulo/<int:pk>/', DeleteArticuloView.as_view(), name='Eliminar Articulo'),
               path('detailarticulo/<int:pk>/', DetailArticuloView.as_view(), name='Detalle Articulo'),
               path('adquisiciónxarticulos/<int:pk>/', views.AdquisicionxArticulos, name='Detalle Adquisicion-Articulos'),
               path('pedidoxarticulos/<int:pk>/', views.PedidoxArticulos, name='Detalle Pedido-Articulos'),

               # Section - Adquisiciones
               path('adquisiciones/', views.vAdquisicion, name='Adquisicion'),
               path('adquisicionesArt/', views.vAdquisicion_Articulos, name='Adquisicion_Articulos'),
               path('adquisicionesPisc/', views.vAdquisicion_Piscinas, name='Adquisicion Piscinas'),
               path('histadquisiciones/', views.Historico_Adquisiciones, name='Historico Adquisicion'),
               path('newadquisicion/', AdquisicionCreateView.as_view(), name='Nueva Adquisicion'),
               path('newadquisicionart/', views.Adqui_ArtCreateView.as_view(), name='Nueva Adquisicion Articulo'),
               path('newadquisicionpisc/', views.Adqui_PiscCreateView.as_view(), name='Nueva Adquisicion Piscina'),
               path('modadquisicion/<int:pk>/', UpdateAdquisicionView.as_view(), name='Modificar Adquisicion'),
               path('modadqarticulo/<int:pk>/', ModAdqArticulosView.as_view(), name='Modificar Adquisicion Articulo'),
               path('modadqpiscina/<int:pk>/', ModAdqPiscinasView.as_view(), name='Modificar Adquisicion Piscina'),
               path('deleteadquisicion/<int:pk>/', views.DeleteAdquisicionView.as_view(), name='Eliminar Adquisicion'),
               path('deleteadqarticulo/<int:pk>/', DeleteAdqArticuloView.as_view(), name='Eliminar Adquisicion Articulo'),
               path('deleteadqpiscina/<int:pk>/', DeleteAdqPiscinaView.as_view(), name='Eliminar Adquisicion Piscina'),
               path('detailadq/<int:pk>/', views.AdquisicionxTotalForm, name='Detalle Adquisicion'),
               path('detailadqart/<int:pk>/', views.AdquisicionxArticuloForm, name='Detalle_Adquisicion_Articulos'),
               path('detailadqpisc/<int:pk>/', views.AdquisicionxPiscinaForm, name='Detalle Adquisicion Piscinas'),
               path('adquisiciones/en_proceso', views.Adquisicion_PR, name='Adquisiciones en Proceso'),
               path('adquisiciones/armado', views.Adquisicion_AR, name='Adquisiciones armadas'),
               path('adquisiciones/en_entrega', views.Adquisicion_EN, name='Adquisiciones en entrega'),
               path('adquisiciones/despachado', views.Adquisicion_DE, name='Adquisiciones despachadas'),
               path('adquisiciones/cancelado', views.Adquisicion_CA, name='Adquisiciones canceladas'),
               path('adquisicionxpago/<int:pk>/', views.AdquisicionxMetodoPago, name='Adquisiciones x Metodo de Pago'),

               # Section - Pedidos
               path('pedidos/', views.vPedidos, name='Pedidos'),
               path('pedidosArt/', views.vPedidos_Articulos, name='Pedidos Articulps'),
               path('pedidosPisc/', views.vPedidos_Piscinas, name='Pedidos Piscinas'),
               path('histpedidos/', views.Historico_Pedidos, name='Historico Pedidos'),
               path('newpedido/', PedidoCreateView.as_view(), name='Nuevo Pedido'),
               path('newpedidoarticulo/', views.Pedido_ArtCreateView.as_view(), name='Nuevo Pedido Articulo'),
               path('newpedidopiscina/', views.Pedido_PiscCreateView.as_view(), name='Nuevo Pedido Piscinas'),
               path('modpedido/<int:pk>/', UpdatePedidoView.as_view(), name='Modificar Pedido'),
               path('modpedidoarticulo/<int:pk>/', ModPedidoArticulosView.as_view(), name='Modificar Pedido Articulo'),
               path('modpedidopiscina/<int:pk>/', ModPedidoPiscinasView.as_view(), name='Modificar Pedido Piscinas'),
               path('deletepedido/<int:pk>/', DeletePedidoView.as_view(), name='Eliminar Pedido'),
               path('deletepedidoarticulo/<int:pk>/', DeletePedidoArticulosView.as_view(), name='Eliminar Pedido Articulo'),
               path('deletepedidopiscina/<int:pk>/', DeletePedidoPiscinasView.as_view(), name='Eliminar Pedido Piscinas'),
               path('detailped/<int:pk>/', views.PedidoxTotalForm, name='DetallePedido'),
               path('detailpedart/<int:pk>/', views.PedidoxArticuloForm, name='Detalle Pedido Articulos'),
               path('detailpedpisc/<int:pk>/', views.PedidoxPiscinaForm, name='Detalle Pedido Piscinas'),
               path('pedidos/en_proceso', views.Pedidos_PR, name='Pedidos en Proceso'),
               path('pedidos/armado', views.Pedidos_AR, name='Pedidos armados'),
               path('pedidos/en_entrega', views.Pedidos_EN, name='Pedidos en entrega'),
               path('pedidos/despachado', views.Pedidos_DE, name='Pedidos despachados'),
               path('pedidos/cancelado', views.Pedidos_CA, name='Pedidos cancelados'),
               path('pedidoxpago/<int:pk>/', views.PedidoxMetodoPago, name='Pedidos x Metodo de Pago'),

               # Section - Caja
               path('caja/', views.vCaja, name='Caja'),
               path('histcaja/', views.Historico_Caja, name='Historico - Caja'),
               path('ingresos/', views.vIngreso, name='Ingreso'),
               path('egresos/', views.vEgreso, name='Egreso'),
               path('newingreso/', views.IngresosCreateView.as_view(), name='Nuevo Ingreso'),
               path('newegreso/', views.EgresosCreateView.as_view(), name='Nuevo Egreso'),
               path('modcaja/<int:pk>/', ModCajaView.as_view(), name='Modificar Caja'),
               path('modingreso/<int:pk>/', UpdateIngresoView.as_view(), name='Modificar ingreso'),
               path('modegreso/<int:pk>/', UpdateEgresoView.as_view(), name='Modificar egreso'),
               path('modingreso_object/<int:pk>/', ModIngresoView.as_view(), name='Modificar Adquisicion'),
               path('modegreso_object/<int:pk>/', ModEgresoView.as_view(), name='Modificar Adquisicion'),
               path('deletecaja/<int:pk>/', DeleteCajaView.as_view(), name='Eliminar Caja'),
               path('deleteingreso/<int:pk>/', DeleteIngresoView.as_view(), name='Eliminar Ingreso'),
               path('deleteegreso/<int:pk>/', DeleteEgresoView.as_view(), name='Eliminar Egreso'),
               path('detailcaja_ingreso/<int:pk>/', views.CajaxIngreso, name='Caja Detalle2'),
               path('detailcaja_egreso/<int:pk>/', views.CajaxEgreso, name='Caja Detalle3'),
               path('ingresos/en_tramite', views.Ingreso_TR, name='Ingresos en Tramite'),
               path('ingresos/impago', views.Ingreso_IM, name='Ingresos impagos'),
               path('ingresos/pagado', views.Ingreso_PA, name='Ingresos pagados'),
               path('egresos/en_tramite', views.Egreso_TR, name='Egresos en Tramite'),
               path('egresos/impago', views.Egreso_IM, name='Egresos impagos'),
               path('egresos/pagado', views.Egreso_PA, name='Egresos pagados'),

               # PDF
               path('articulosxCategoriaPDF/<int:pk>/', ArticulosxCategoriaPDF.as_view(), name='PDF - Articulos x Categoria'),
               path('clientePDF/', ClientePDF.as_view(), name='PDF - Clientes'),
               path('pedidosxClientePDF/<int:pk>/', PedidosxClientePDF.as_view(), name='PDF - Pedido x Cliente'),
               path('proveedorPDF/', ProveedorPDF.as_view(), name='PDF - Proveedor'),
               path('adquisicionesxProveedorPDF/<int:pk>/', AdquisicionesxProveedorPDF.as_view(), name='PDF - Adquisiciones x Proveedor'),
               path('empleadoPDF/', EmpleadoPDF.as_view(), name='PDF - Empleado'),
               path('empleadoAdministrativoPDF/', Empleado_AdministrativoPDF.as_view(), name='PDF - Empleado Administrativo'),
               path('empleadoObreroPDF/', Empleado_ObreroPDF.as_view(), name='PDF - Empleado Obrero'),
               path('empleadoTemporarioPDF/', Empleado_TemporarioPDF.as_view(), name='PDF - Empleado Temporario'),
               path('empleadoGerenciaPDF/', Empleado_GerenciaPDF.as_view(), name='PDF - Empleado Gerencia'),
               path('empleadoVentasPDF/', Empleado_VentasPDF.as_view(), name='PDF - Empleado Ventas'),
               path('empleadoLogisticaPDF/', Empleado_LogisticaPDF.as_view(), name='PDF - Empleado Logistica'),
               path('cajaxEmpleadoPDF/<int:pk>/', CajaxEmpleadoPDF.as_view(), name='PDF - Caja x Empleado'),
               path('obraPDF/', ObraPDF.as_view(), name='PDF - Obra'),
               path('articulosPDF/', ArticulosPDF.as_view(), name='PDF - Articulos'),
               path('adquisicionxArticuloPDF/<int:pk>/', AdquisicionesxArticulosPDF.as_view(), name='PDF - Adquisicion x Articulo'),
               path('pedidoxArticuloPDF/<int:pk>/', PedidosxArticulosPDF.as_view(), name='PDF - Pedido x Articulo'),
               path('piscinasPDF/', PiscinasPDF.as_view(), name='PDF - Piscinas'),
               path('adquisicionxPiscinaPDF/<int:pk>/', AdquisicionesxPiscinasPDF.as_view(), name='PDF - Adquisicion x Piscina'),
               path('pedidoxPiscinaPDF/<int:pk>/', PedidosxPiscinasPDF.as_view(), name='PDF - Pedido x Piscina'),
               path('adquisicionPDF/', AdquisicionPDF.as_view(), name='PDF - Adquisicion'),
               path('adquisicion_ArticuloPDF/', Adquisicion_ArticuloPDF.as_view(), name='PDF - Adquisicion'),
               path('adquisicion_PiscinaPDF/', Adquisicion_PiscinaPDF.as_view(), name='PDF - Adquisicion'),
               path('adquisicionxPagoPDF/<int:pk>/', AdquisicionxPagoPDF.as_view(), name='PDF - Adquisicion x Pago'),
               path('pedidoxPagoPDF/<int:pk>/', PedidoxPagoPDF.as_view(), name='PDF - Pedido x Pago'),
               path('adquisicionARPDF/', Adquisicion_ARPDF.as_view(), name='PDF - Adquisicion armada'),
               path('adquisicionCAPDF/', Adquisicion_CAPDF.as_view(), name='PDF - Adquisicion armada'),
               path('adquisicionDEPDF/', Adquisicion_DEPDF.as_view(), name='PDF - Adquisicion armada'),
               path('adquisicionENPDF/', Adquisicion_ENPDF.as_view(), name='PDF - Adquisicion armada'),
               path('adquisicionPRPDF/', Adquisicion_PRPDF.as_view(), name='PDF - Adquisicion armada'),
               path('pedidoPDF/', PedidosPDF.as_view(), name='PDF - Pedido'),
               path('pedido_ArticuloPDF/', Pedido_ArticuloPDF.as_view(), name='PDF - Adquisicion'),
               path('pedido_PiscinaPDF/', Pedido_PiscinaPDF.as_view(), name='PDF - Adquisicion'),
               path('pedidoxPagoPDF/<int:pk>/', PedidoxPagoPDF.as_view(), name='PDF - Pedido x Pago'),
               path('pedidoARPDF/', Pedido_ARPDF.as_view(), name='PDF - Pedido armado'),
               path('pedidoCAPDF/', Pedido_CAPDF.as_view(), name='PDF - Pedido armada'),
               path('pedidoDEPDF/', Pedido_DEPDF.as_view(), name='PDF - Pedido armada'),
               path('pedidoENPDF/', Pedido_ENPDF.as_view(), name='PDF - Pedido armada'),
               path('pedidoPRPDF/', Pedido_PRPDF.as_view(), name='PDF - Pedido armada'),
               path('ingresosPDF/', IngresosPDF.as_view(), name='PDF - Pedido'),
               path('ingresosPAPDF/', IngresosPAPDF.as_view(), name='PDF - Pedido'),
               path('ingresosIMPDF/', IngresosIMPDF.as_view(), name='PDF - Pedido'),
               path('ingresosTRPDF/', IngresosTRPDF.as_view(), name='PDF - Pedido'),
               path('egresosPDF/', EgresosPDF.as_view(), name='PDF - Adquisicion'),
               path('egresosPAPDF/', EgresosPAPDF.as_view(), name='PDF - Adquisicion'),
               path('egresosIMPDF/', EgresosIMPDF.as_view(), name='PDF - Adquisicion'),
               path('egresosTRPDF/', EgresosTRPDF.as_view(), name='PDF - Adquisicion'),

               # Graficos
               path('graficos/', views.grafico_one, name='Graficos'),
               path('graficos2/', views.grafico_two, name='Graficos 2'),
               path('graficos3/', views.grafico_three, name='Graficos 3'),
               path('graficos4/', views.grafico_four, name='Graficos 4'),
               path('graficos5/', views.grafico_five, name='Graficos 5'),
               ]