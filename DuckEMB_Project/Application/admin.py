"""
Application/admin.py

Se encarga de leer los metadatos de sus modelos para proporcionar una interfaz rápida y
centrada en el modelo donde los usuarios de confianza pueden administrar el contenido de su sitio.
El uso recomendado por el administrador se limita a la herramienta de gestión interna de una organización.

Para obtener más información sobre este archivo, consulte:
https://docs.djangoproject.com/en/4.1/ref/contrib/admin/
"""

from django.contrib import admin
from .models import Piscinas, Categorias, Articulos, Provincias, Clientes, Direccion_Cliente, \
    Proveedores, Direccion_Proveedor, Empleados, Direccion_Empleado, Metodos_Pagos, Pedidos, Obras, Direccion_Obras, \
    Caja, Egresos, Ingresos, AdquisicionProveedor_Articulos, AdquisicionProveedor_Piscinas, Pedidos_Articulos, \
    Pedidos_Piscinas, Adquisicion

# Register your models here.

def armado(modeladmin, request, queryset):
    """Esta función actualizará el campo 'estado' de un conjunto de objetos seleccionados en la interfaz de administración
        de Django con el valor 'AR'.

    Args:
        modeladmin: Define la interfaz de administración del modelo. Este parámetro permite acceder a las propiedades y métodos de la clase ModelAdmin, como el nombre del modelo o los campos a mostrar en la lista de objetos.
        request (object): Sirve para entregar los objetos que contienen los metadatos de la solicitud que van a ser enviado a la plantilla.
        queryset: Permite realizar operaciones en bloque sobre un conjunto de objetos.

    Returns:
        Actualiza el estado de los objetos seleccionador a 'AR'.
    """
    queryset.update(estado= 'AR')


def entregable(modeladmin, request, queryset):
    """Esta función actualizará el campo 'estado' de un conjunto de objetos seleccionados en la interfaz de administración
        de Django con el valor 'EN'.

    Args:
        modeladmin: Define la interfaz de administración del modelo. Este parámetro permite acceder a las propiedades y métodos de la clase ModelAdmin, como el nombre del modelo o los campos a mostrar en la lista de objetos.
        request (object): Sirve para entregar los objetos que contienen los metadatos de la solicitud que van a ser enviado a la plantilla.
        queryset: Permite realizar operaciones en bloque sobre un conjunto de objetos.

    Returns:
        Actualiza el estado de los objetos seleccionador a 'EN'.
    """
    queryset.update(estado= 'EN')


def despachado(modeladmin, request, queryset):
    """Esta función actualizará el campo 'estado' de un conjunto de objetos seleccionados en la interfaz de administración
        de Django con el valor 'DE'.

    Args:
        modeladmin: Define la interfaz de administración del modelo. Este parámetro permite acceder a las propiedades y métodos de la clase ModelAdmin, como el nombre del modelo o los campos a mostrar en la lista de objetos.
        request (object): Sirve para entregar los objetos que contienen los metadatos de la solicitud que van a ser enviado a la plantilla.
        queryset: Permite realizar operaciones en bloque sobre un conjunto de objetos.

    Returns:
        Actualiza el estado de los objetos seleccionador a 'DE'.
    """
    queryset.update(estado= 'DE')


def impago(modeladmin, request, queryset):
    """Esta función actualizará el campo 'condicion' de un conjunto de objetos seleccionados en la interfaz de administración
        de Django con el valor 'IM'.

    Args:
        modeladmin: Define la interfaz de administración del modelo. Este parámetro permite acceder a las propiedades y métodos de la clase ModelAdmin, como el nombre del modelo o los campos a mostrar en la lista de objetos.
        request (object): Sirve para entregar los objetos que contienen los metadatos de la solicitud que van a ser enviado a la plantilla.
        queryset: Permite realizar operaciones en bloque sobre un conjunto de objetos.

    Returns:
        Actualiza la condicion de los objetos seleccionador a 'IM'.
    """
    queryset.update(condicion= 'IM')


def pagado(modeladmin, request, queryset):
    """Esta función actualizará el campo 'condicion' de un conjunto de objetos seleccionados en la interfaz de administración
        de Django con el valor 'PA'.

    Args:
        modeladmin: Define la interfaz de administración del modelo. Este parámetro permite acceder a las propiedades y métodos de la clase ModelAdmin, como el nombre del modelo o los campos a mostrar en la lista de objetos.
        request (object): Sirve para entregar los objetos que contienen los metadatos de la solicitud que van a ser enviado a la plantilla.
        queryset: Permite realizar operaciones en bloque sobre un conjunto de objetos.

    Returns:
        Actualiza la condicion de los objetos seleccionador a 'PA'.
    """
    queryset.update(condicion= 'PA')


# Descripcion de los estados establecidos.
armado.short_description = 'Armar los pedidos/ Armando las adquisiciones - Seleccionados'
entregable.short_description = 'Entregar pedidos/ En entrega de las adquisiciones - Seleccionados'
despachado.short_description = 'Despachar pedidos/ Adquisiciones despachadas - Seleccionados'
impago.short_description = 'Declarar - Impago'
pagado.short_description = 'Declarar - Pagado'


class Pedidos_ArticulosInline(admin.TabularInline):
    """Esta función define una clase que se utiliza en Django para mostrar el modelo 'Pedidos_Articulos' relacionado en línea dentro del formulario de edición del otro modelo 'Pedidos'.

    Args:
        TabularInline (class): Se utiliza para mostrar una tabla en línea con los datos de los objetos relacionados.

    Parameters:
        model: Es el modelo que se desea mostrar en línea.
        extra: es el número de objetos adicionales que se mostrarán en línea.
    """
    model = Pedidos_Articulos
    extra = 1


class Pedidos_PiscinasInline(admin.TabularInline):
    """Esta función define una clase que se utiliza en Django para mostrar el modelo 'Pedidos_Piscinas' relacionado en línea dentro del formulario de edición del otro modelo 'Pedidos'.

    Args:
        TabularInline (class): Se utiliza para mostrar una tabla en línea con los datos de los objetos relacionados.

    Parameters:
        model: Es el modelo que se desea mostrar en línea.
        extra: es el número de objetos adicionales que se mostrarán en línea.
    """
    model = Pedidos_Piscinas
    extra = 1


class AdquisicionProveedor_PiscinasInline(admin.TabularInline):
    """Esta función define una clase que se utiliza en Django para mostrar el modelo 'AdquisicionProveedor_Piscinas' relacionado en línea dentro del formulario de edición del otro modelo 'Adquisiciones'.

    Args:
        TabularInline (class): Se utiliza para mostrar una tabla en línea con los datos de los objetos relacionados.

    Parameters:
        model: Es el modelo que se desea mostrar en línea.
        extra: es el número de objetos adicionales que se mostrarán en línea.
    """
    model = AdquisicionProveedor_Piscinas
    extra = 1


class AdquisicionProveedor_ArticulosInline(admin.TabularInline):
    """Esta función define una clase que se utiliza en Django para mostrar el modelo 'AdquisicionProveedor_Articulos' relacionado en línea dentro del formulario de edición del otro modelo 'Adquisiciones'.

    Args:
        TabularInline (class): Se utiliza para mostrar una tabla en línea con los datos de los objetos relacionados.

    Parameters:
        model: Es el modelo que se desea mostrar en línea.
        extra: es el número de objetos adicionales que se mostrarán en línea.
    """
    model = AdquisicionProveedor_Articulos
    extra = 1


class Direccion_ClienteInline(admin.TabularInline):
    """Esta función define una clase que se utiliza en Django para mostrar el modelo 'Direccion_Cliente' relacionado en línea dentro del formulario de edición del otro modelo 'Clientes'.

    Args:
        TabularInline (class): Se utiliza para mostrar una tabla en línea con los datos de los objetos relacionados.

    Parameters:
        model: Es el modelo que se desea mostrar en línea.
        extra: es el número de objetos adicionales que se mostrarán en línea.
    """
    model = Direccion_Cliente
    extra = 1


class Direccion_EmpleadosInline(admin.TabularInline):
    """Esta función define una clase que se utiliza en Django para mostrar el modelo 'Direccion_Empleado' relacionado en línea dentro del formulario de edición del otro modelo 'Empleado'.

    Args:
        TabularInline (class): Se utiliza para mostrar una tabla en línea con los datos de los objetos relacionados.

    Parameters:
        model: Es el modelo que se desea mostrar en línea.
        extra: es el número de objetos adicionales que se mostrarán en línea.
    """
    model = Direccion_Empleado
    extra = 1


class Direccion_ProveedoresInline(admin.TabularInline):
    """Esta función define una clase que se utiliza en Django para mostrar el modelo 'Direccion_Proveedor' relacionado en línea dentro del formulario de edición del otro modelo 'Proveedores'.

    Args:
        TabularInline (class): Se utiliza para mostrar una tabla en línea con los datos de los objetos relacionados.

    Parameters:
        model: Es el modelo que se desea mostrar en línea.
        extra: es el número de objetos adicionales que se mostrarán en línea.
    """
    model = Direccion_Proveedor
    extra = 1


class Direccion_ObrasInline(admin.TabularInline):
    """Esta función define una clase que se utiliza en Django para mostrar el modelo 'Direccion_Obras' relacionado en línea dentro del formulario de edición del otro modelo 'Obras'.

    Args:
        TabularInline (class): Se utiliza para mostrar una tabla en línea con los datos de los objetos relacionados.

    Parameters:
        model: Es el modelo que se desea mostrar en línea.
        extra: es el número de objetos adicionales que se mostrarán en línea.
    """
    model = Direccion_Obras
    extra = 1


class IngresosInline(admin.TabularInline):
    """Esta función define una clase que se utiliza en Django para mostrar el modelo 'Ingresos' relacionado en línea dentro del formulario de edición del otro modelo 'Caja'.

    Args:
        TabularInline (class): Se utiliza para mostrar una tabla en línea con los datos de los objetos relacionados.

    Parameters:
        model: Es el modelo que se desea mostrar en línea.
        extra: es el número de objetos adicionales que se mostrarán en línea.
    """
    model = Ingresos
    extra = 1


class EgresosInline(admin.TabularInline):
    """Esta función define una clase que se utiliza en Django para mostrar el modelo 'Egresos' relacionado en línea dentro del formulario de edición del otro modelo 'Caja'.

    Args:
        TabularInline (class): Se utiliza para mostrar una tabla en línea con los datos de los objetos relacionados.

    Parameters:
        model: Es el modelo que se desea mostrar en línea.
        extra: es el número de objetos adicionales que se mostrarán en línea.
    """
    model = Egresos
    extra = 1


class adminPiscinas(admin.ModelAdmin):
    list_display = ('descripcion', 'unidades', 'base', 'sf_casilla', 'ac', 'al', 'ah', 'mam', 'total')   # --> Display de campos que se muestran.


class adminProvincia(admin.ModelAdmin):
    ordering = ['provincia'] # --> Ordenamiento bajo el campo seleccionado.


class adminArticulos(admin.ModelAdmin):
    list_display = ('descripcion', 'precio', 'iva', 'stock', 'categoria', 'marca', 'modelo', 'imagen')
    list_filter = ('categoria', 'marca')   # --> Filtro de contenido por campos seleccionados.


class adminClientes(admin.ModelAdmin):
    inlines = [Direccion_ClienteInline,]   # --> Tabla intermedia - Direccion del cliente dentro de "Clientes".
    list_display = ('dni', 'nombre', 'telefono', 'email')


class adminDireccion_Cliente(admin.ModelAdmin):
    list_display = ('idCliente', 'calle', 'barrio', 'ciudad', 'cp', 'provincia')
    list_filter = ('ciudad', 'provincia', 'cp')


class adminProveedores(admin.ModelAdmin):
    inlines = [Direccion_ProveedoresInline,]   # --> Tabla intermedia - Direccion del proveedor dentro de "Proveedores".
    list_display = ('cuit', 'nombre', 'telefono', 'email')
    search_fields = ['nombre']


class adminDireccion_Proveedor(admin.ModelAdmin):
    list_display = ('idProveedor', 'calle', 'barrio', 'ciudad', 'cp', 'provincia')
    list_filter = ('ciudad', 'provincia', 'cp')


class adminEmpleados(admin.ModelAdmin):
    inlines = [Direccion_EmpleadosInline,]    # --> Tabla intermedia - Direccion del empleado dentro de "Empleados".
    list_display = ('dni', 'nombre', 'telefono', 'email', 'rol')
    list_filter = ('rol',)


class adminDireccion_Empleado(admin.ModelAdmin):
    list_display = ('idEmpleado', 'calle', 'barrio', 'ciudad', 'cp', 'provincia')


class adminMetodos_Pagos(admin.ModelAdmin):
    list_display = ('descripcion', 'unidades')


class adminPedidos(admin.ModelAdmin):
    inlines = [Pedidos_ArticulosInline, Pedidos_PiscinasInline,]
    list_display = ('idCliente', 'estado')
    list_filter = ('idCliente', 'estado')
    actions = (armado, entregable, despachado)


class adminObras(admin.ModelAdmin):
    inlines = [Direccion_ObrasInline,]    # --> Tabla intermedia - Direccion de la obra dentro de "Obras".
    list_display = ('fechaInicio', 'fechaFinal', 'numeroPedido', 'idEmpleado')
    list_filter = ('fechaInicio', 'idEmpleado')


class adminDireccion_Obras(admin.ModelAdmin):
    list_display = ('idObra', 'calle', 'barrio', 'ciudad', 'cp', 'provincia')
    list_filter = ('ciudad', 'provincia', 'cp')


class adminCaja(admin.ModelAdmin):
    inlines = [IngresosInline, EgresosInline]
    list_display = ('fecha', 'idEmpleado')
    list_filter = ('fecha',)


class adminEgresos(admin.ModelAdmin):
    list_display = ('metodoPago', 'valor', 'idCaja', 'condicion')
    list_filter = ('metodoPago', 'condicion')
    actions = (impago, pagado)


class adminIngresos(admin.ModelAdmin):
    list_display = ('metodoPago', 'valor', 'idCaja', 'idPedido', 'condicion')
    list_filter = ('metodoPago', 'condicion')
    actions = (impago, pagado)


class adminAdquisicion(admin.ModelAdmin):
    inlines = [AdquisicionProveedor_ArticulosInline, AdquisicionProveedor_PiscinasInline]
    actions = (armado, entregable, despachado)


class adminAdquisicionProveedor_Articulos(admin.ModelAdmin):
    list_display = ('unidades', 'idArticulo')


class adminAdquisicionProveedor_Piscinas(admin.ModelAdmin):
    list_display = ('unidades', 'idPiscina')


class adminPedidos_Articulos(admin.ModelAdmin):
    list_display = ('unidades', 'idPedido', 'idArticulo')


class adminPedidos_Piscinas(admin.ModelAdmin):
    list_display = ('unidades', 'idPedido', 'idPiscina')


admin.site.register(Piscinas, adminPiscinas)
admin.site.register(Categorias)
admin.site.register(Articulos, adminArticulos)
admin.site.register(Provincias, adminProvincia)
admin.site.register(Clientes, adminClientes)
admin.site.register(Direccion_Cliente, adminDireccion_Cliente)
admin.site.register(Proveedores, adminProveedores)
admin.site.register(Direccion_Proveedor, adminDireccion_Proveedor)
admin.site.register(Empleados, adminEmpleados)
admin.site.register(Direccion_Empleado, adminDireccion_Empleado)
admin.site.register(Metodos_Pagos)
admin.site.register(Pedidos, adminPedidos)
admin.site.register(Obras, adminObras)
admin.site.register(Direccion_Obras, adminDireccion_Obras)
admin.site.register(Caja, adminCaja)
admin.site.register(Ingresos, adminIngresos)
admin.site.register(Egresos, adminEgresos)
admin.site.register(AdquisicionProveedor_Articulos, adminAdquisicionProveedor_Articulos)
admin.site.register(AdquisicionProveedor_Piscinas, adminAdquisicionProveedor_Piscinas)
admin.site.register(Pedidos_Articulos, adminPedidos_Articulos)
admin.site.register(Pedidos_Piscinas, adminPedidos_Piscinas)
admin.site.register(Adquisicion, adminAdquisicion)