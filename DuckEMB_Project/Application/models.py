"""
models.py

Es la fuente única y definitiva de información sobre sus datos. Contiene los campos y comportamientos
esenciales de los datos que está almacenando.

Para obtener más información sobre este archivo, consulte:
https://docs.djangoproject.com/en/4.1/topics/db/models/
"""

from django.db import models
from django.db.models import Sum
from decimal import Decimal
from django.db import models
from model_utils import Choices
from datetime import date

import requests

def consultar_dolar():
    response = requests.get('https://www.dolarsi.com/api/api.php?type=dolar')
    data = response.json()
    dolar_oficial = None
    for casa in data:
        if casa['casa']['nombre'] == 'Oficial':
            dolar_oficial = casa['casa']
            break
    if dolar_oficial is not None:
        venta = dolar_oficial['venta']
        return venta
    else:
        print('No se encontró el dólar oficial')

ORDER_COLUMN_CHOICES_CAJA = Choices(
    ('0', 'fecha'),
    ('1', 'recaudacion'),
    ('2', 'idEmpleado'),
)

# Create your models here.
class Piscinas(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=60, help_text='Descripción de la piscina', verbose_name='Descripción')
    unidades = models.IntegerField(help_text='Unidades', verbose_name='Unidades')
    base = models.IntegerField(verbose_name='BASE')
    sf_casilla = models.IntegerField(verbose_name='SF Casilla')
    ac = models.IntegerField(verbose_name='AC')
    al = models.IntegerField(verbose_name='AL')
    ah = models.IntegerField(verbose_name='AH')
    mam = models.IntegerField(verbose_name='M-A-M')
    imagen = models.ImageField(upload_to='Images/Piscinas', help_text='Imagen del articulo', verbose_name='Imagen', blank=True, default='emb-logo.png')
    pedidosPisc = models.ManyToManyField('Pedidos', through='Pedidos_Piscinas')
    adquisicionPisc = models.ManyToManyField('Adquisicion', through='AdquisicionProveedor_Piscinas')

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en el atributo 'descripcion' de la clase 'Piscinas'.
        """

        return str(self.descripcion)

    def _get_total(self):
        return self.base + self.sf_casilla + self.ac + self.al + self.ah + self.mam
    total = property(_get_total)

    def _get_base_dolar(self):
        dolar = consultar_dolar()
        valor = float(dolar.replace(',', '.'))
        return self.base * valor
    base_dolar = property(_get_base_dolar)

    def _get_total_dolar(self):
        dolar = consultar_dolar()
        valor = float(dolar.replace(',', '.'))
        return self.total * valor
    total_dolar = property(_get_total_dolar)


class Categorias(models.Model):
    categoria = models.CharField(max_length=30, verbose_name='Categoria')
    imagen = models.ImageField(upload_to='Images/Categorias', help_text='Imagen del articulo', verbose_name='Imagen', blank=True, default='emb-logo.png')

    def __str__(self):
        return str(self.categoria)

class Articulos(models.Model):
    descripcion = models.CharField(max_length=60, verbose_name='Descripción')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    porcentaje = models.DecimalField(max_digits=3, decimal_places=2, help_text='Equivalencia: 1.00 = 100%')
    stock = models.IntegerField(verbose_name='Stock')
    marca = models.CharField(max_length=30, verbose_name='Marca')
    modelo = models.CharField(max_length=60, verbose_name='Modelo', blank=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, verbose_name='Categoria')
    imagen = models.ImageField(upload_to='Images/Articulos', verbose_name='Imagen', blank=True, default='emb-logo.png')
    pedidosArtic = models.ManyToManyField('Pedidos', through='Pedidos_Articulos')

    def _get_precio_venta(self):
        number_porcentaje = Decimal(1 + self.porcentaje)
        return self.precio * number_porcentaje
    venta = property(_get_precio_venta)

    def _get_precio_iva(self):
        number_iva = Decimal(1.21)
        return self.venta * number_iva
    iva = property(_get_precio_iva)

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en los atributos 'descripcion' y 'marca' de la clase 'Articulos'.
        """
        return str(self.descripcion) + ' (' + str(self.marca) + ')'

class Provincias(models.Model):
    provincia = models.CharField(max_length=40, verbose_name='Provincia')

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en el atributo 'provincia' de la clase 'Provincias'.
        """
        return str(self.provincia)

class Clientes(models.Model):
    dni = models.CharField(primary_key=True, max_length=9, help_text='Numero de Identidad', verbose_name='DNI')
    nombre = models.CharField(max_length=50, help_text='Nombre del Cliente', verbose_name='Nombre', blank=True)
    telefono = models.CharField(max_length=14, help_text='Telefono del Cliente', verbose_name='Telefono', blank=True)
    email = models.EmailField(help_text='e-Mail del Cliente', verbose_name='e-Mail', blank=True)
    imagen = models.ImageField(upload_to='Images/Clientes', help_text='Imagen del articulo', verbose_name='Imagen', blank=True, default='emb-logo.png')

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en los atributos 'nombre' y 'dni' de la clase 'Clientes'.
        """
        return str(self.nombre) + ' (' + str(self.dni) + ')'

class Direccion_Cliente(models.Model):
    idCliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True, blank=True, help_text='Cliente', verbose_name='Cliente')
    calle = models.CharField(max_length=100, help_text='Calle', verbose_name='Calle', blank=True)
    barrio = models.CharField(max_length=40, help_text='Barrio', verbose_name='Barrio', blank=True)
    ciudad = models.CharField(max_length=40, help_text='Ciudad', verbose_name='Ciudad', blank=True)
    cp = models.IntegerField(help_text='Codigo Postal', verbose_name='CP', blank=True)
    provincia = models.ForeignKey(Provincias, on_delete=models.CASCADE, verbose_name='Provincia', blank=True)

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en el atributo 'idCliente' de la clase 'Direccion_Cliente'.
        """
        return str(self.idCliente)

class Proveedores(models.Model):
    cuit = models.CharField(primary_key=True, max_length=12, help_text='Numero de Identidad', verbose_name='CUIT')
    nombre = models.CharField(max_length=50, help_text='Nombre del Proveedor', verbose_name='Nombre', blank=True)
    telefono = models.CharField(max_length=14, help_text='Telefono del Proveedor', verbose_name='Telefono', blank=True)
    email = models.EmailField(help_text='e-Mail del Proveedor', verbose_name='e-Mail', blank=True)
    imagen = models.ImageField(upload_to='Images/Proveedores', help_text='Imagen del articulo', verbose_name='Imagen', blank=True, default='emb-logo.png')

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en los atributos 'nombre' y 'cuit' de la clase 'Proveedores'.
        """
        return str(self.nombre) + ' (' + str(self.cuit) + ')'

class Direccion_Proveedor(models.Model):
    idProveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, help_text='Proveedor', verbose_name='Proveedor')
    calle = models.CharField(max_length=100, help_text='Calle', verbose_name='Calle', blank=True)
    barrio = models.CharField(max_length=40, help_text='Barrio', verbose_name='Barrio', blank=True)
    ciudad = models.CharField(max_length=40, help_text='Ciudad', verbose_name='Ciudad', blank=True)
    cp = models.IntegerField(help_text='Codigo Postal', verbose_name='CP', blank=True)
    provincia = models.ForeignKey(Provincias, on_delete=models.CASCADE, verbose_name='Provincia', blank=True)

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en el atributo 'idProveedor' de la clase 'Direccion_Proveedor'.
        """
        return str(self.idProveedor)

class Empleados(models.Model):
    ADMINISTRATIVO = 'AD'
    OBRERO = 'OB'
    TEMPORARIO = 'TE'
    GERENCIA = 'GE'
    VENTAS = 'VE'
    LOGISTICA = 'LO'
    ROL =  [
        (ADMINISTRATIVO, 'Administrativo'),
        (OBRERO, 'Obrero'),
        (TEMPORARIO, 'Temporario'),
        (GERENCIA, 'Gerencia'),
        (VENTAS, 'Ventas'),
        (LOGISTICA, 'Logistica')
    ]
    dni = models.CharField(primary_key=True, max_length=9, help_text='Numero de Identidad', verbose_name='DNI')
    nombre = models.CharField(max_length=50, help_text='Nombre del Empleado', verbose_name='Nombre')
    telefono = models.CharField(max_length=14, help_text='Telefono del Empleado', verbose_name='Telefono', blank=True)
    email = models.EmailField(help_text='e-Mail del Empleado', verbose_name='e-Mail', blank=True)
    rol = models.CharField(max_length=20, verbose_name='Rol', choices=ROL)
    imagen = models.ImageField(upload_to='Images/Empleados', help_text='Imagen del articulo', verbose_name='Imagen', blank=True, default='emb-logo.png')

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en los atributos 'nombre' y 'rol' de la clase 'Empleados'.
        """
        return str(self.nombre) + ' (' + str(self.rol) + ')'

class Direccion_Empleado(models.Model):
    idEmpleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, help_text='Empleado', verbose_name='Empleado')
    calle = models.CharField(max_length=100, help_text='Calle', verbose_name='Calle', blank=True)
    barrio = models.CharField(max_length=40, help_text='Barrio', verbose_name='Barrio', blank=True)
    ciudad = models.CharField(max_length=40, help_text='Ciudad', verbose_name='Ciudad', blank=True)
    cp = models.IntegerField(help_text='Codigo Postal', verbose_name='CP', blank=True)
    provincia = models.ForeignKey(Provincias, on_delete=models.CASCADE, verbose_name='Provincia', blank=True)

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en el atributo 'idEmpleado' de la clase 'Direccion_Empleado'.
        """
        return str(self.idEmpleado)

class Metodos_Pagos(models.Model):
    metodoPago = models.CharField(max_length=40, verbose_name='Medio de Pago')

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en el atributo 'metodoPago' de la clase 'Metodos_Pagos'.
        """
        return str(self.metodoPago)

class Pedidos(models.Model):
    PROCESO = 'PR'
    ARMADO = 'AR'
    ENTREGABLE = 'EN'
    DESPACHADO = 'DE'
    CANCELADO = 'CA'
    ESTADOS =  [
        (PROCESO, 'En proceso'),
        (ARMADO, 'Armado'),
        (ENTREGABLE, 'En entrega'),
        (DESPACHADO, 'Despachado'),
        (CANCELADO, 'Cancelado')
    ]
    id = models.AutoField(primary_key=True)
    idCliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, help_text='Identificador del Cliente', verbose_name='Cliente')
    metodoPago = models.ForeignKey(Metodos_Pagos, on_delete=models.CASCADE, help_text='Medio de Pago', verbose_name='Medio de Pago')
    estado = models.CharField(max_length= 15, choices=ESTADOS, default=PROCESO)
    fecha = models.DateField(help_text='Fecha del pedido', verbose_name='Fecha', default=date.today)
    piscina = models.ManyToManyField('Piscinas', through='Pedidos_Piscinas')
    articulo = models.ManyToManyField('Articulos', through='Pedidos_Articulos')
    ingreso = models.ManyToManyField('Caja', through='Ingresos')

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en los atributos 'id' y 'fecha' de la clase 'Pedidos'.
        """
        return 'Pedido #' + str(self.id)  + ' - Referente al día: ' + str(self.fecha)

class Adquisicion(models.Model):
    PROCESO = 'PR'
    ARMADO = 'AR'
    ENTREGABLE = 'EN'
    DESPACHADO = 'DE'
    CANCELADO = 'CA'
    ESTADOS =  [
        (PROCESO, 'En proceso'),
        (ARMADO, 'Armado'),
        (ENTREGABLE, 'En entrega'),
        (DESPACHADO, 'Despachado'),
        (CANCELADO, 'Cancelado')
    ]
    id = models.AutoField(primary_key=True)
    idProveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, help_text='Identificador del Proveedor', verbose_name='Proveedor')
    estado = models.CharField(max_length= 15, choices=ESTADOS)
    metodoPago = models.ForeignKey(Metodos_Pagos, on_delete=models.CASCADE, help_text='Medio de Pago', verbose_name='Medio de Pago')
    fechaEntrega = models.DateField(help_text='Fecha de Entrega', verbose_name='Entregado')
    fechaRecibido = models.DateField(help_text='Fecha de Recibo', verbose_name='Recibido', blank=True, null=True)
    piscina = models.ManyToManyField('Piscinas', through='AdquisicionProveedor_Piscinas')
    articulo = models.ManyToManyField('Articulos', through='AdquisicionProveedor_Articulos')
    egreso = models.ManyToManyField('Caja', through='Egresos')

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en los atributos 'id' y 'fechaEntrega' de la clase 'Adquisicion'.
        """
        return 'Adquisicion #' + str(self.id) + ' - Referente al día: ' + str(self.fechaEntrega)

class Obras(models.Model):
    id = models.AutoField(primary_key=True)
    fechaInicio = models.DateField(help_text='Fecha de inicio de Obra', verbose_name='Inicio', blank=True)
    fechaFinal = models.DateField(help_text='Fecha de final de Obra', verbose_name='Final', blank=True, null=True)
    numeroPedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, help_text='Numero de Pedido', verbose_name='Numero de Pedido')
    idEmpleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, help_text='Empleado', verbose_name='Solicitado por:')

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en el atributo 'id' de la clase 'Obras'.
        """
        return 'Obra #' + str(self.id)

class Direccion_Obras(models.Model):
    idObra = models.ForeignKey(Obras, on_delete=models.CASCADE, help_text='Obra', verbose_name='Obra')
    calle = models.CharField(max_length=100, help_text='Calle', verbose_name='Calle', blank=True)
    barrio = models.CharField(max_length=40, help_text='Barrio', verbose_name='Barrio', blank=True)
    ciudad = models.CharField(max_length=40, help_text='Ciudad', verbose_name='Ciudad', blank=True)
    cp = models.IntegerField(help_text='Codigo Postal', verbose_name='CP', blank=True)
    provincia = models.ForeignKey(Provincias, on_delete=models.CASCADE, verbose_name='Provincia', blank=True)

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en el atributo 'idObra' de la clase 'Direccion_Obras'.
        """
        return str(self.idObra)

class Caja(models.Model):
    INGRESO = 'IN'
    EGRESO = 'EG'
    TIPO =  [
        (INGRESO, 'Ingresos'),
        (EGRESO, 'Egresos')
    ]
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(help_text='Fecha', verbose_name='Fecha')
    idEmpleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, help_text='Empleado', verbose_name='Empleado')
    tipo = models.CharField(max_length= 15, choices=TIPO)
    ingresoCaja = models.ManyToManyField('Pedidos', through='Ingresos')
    egresoCaja = models.ManyToManyField('Adquisicion', through='Egresos')

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en el atributo 'fecha' de la clase 'Caja'.
        """
        return str(self.fecha)

class Egresos(models.Model):
    TRAMITE = 'TR'
    IMPAGO = 'IM'
    PAGADO = 'PA'
    CONDICION =  [
        (TRAMITE, 'En tramite'),
        (IMPAGO, 'Impago'),
        (PAGADO, 'Pagado')
    ]
    metodoPago = models.ForeignKey(Metodos_Pagos, on_delete=models.CASCADE, help_text='Medio de Pago', verbose_name='Medio de Pago')
    valor = models.PositiveIntegerField(help_text='Valor ingresado', verbose_name='Valor')
    idCaja = models.ForeignKey(Caja, on_delete=models.CASCADE, verbose_name='Caja')
    condicion = models.CharField(max_length=20, choices=CONDICION, default=TRAMITE)
    idAdquisicion = models.ForeignKey(Adquisicion, on_delete=models.CASCADE, help_text='Adquisicion', verbose_name='Adquisicion')

    def _get_restar(self):
        Valor = self.idCaja.recaudacion
        Valor -= self.valor
        return Valor
    
    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en el atributo 'idCaja' de la clase 'Egresos'.
        """
        return 'Egreso ' + str(self.idCaja)

class Ingresos(models.Model):
    TRAMITE = 'TR'
    IMPAGO = 'IM'
    PAGADO = 'PA'
    CONDICION =  [
        (TRAMITE, 'En tramite'),
        (IMPAGO, 'Impago'),
        (PAGADO, 'Pagado')
    ]
    metodoPago = models.ForeignKey(Metodos_Pagos, on_delete=models.CASCADE, help_text='Medio de Pago', verbose_name='Medio de Pago')
    valor = models.PositiveIntegerField(help_text='Valor ingresado', verbose_name='Valor')
    idCaja = models.ForeignKey(Caja, on_delete=models.CASCADE, verbose_name='Caja')
    idPedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, help_text='Pedido', verbose_name='Pedido')
    condicion = models.CharField(max_length=20, choices=CONDICION, default=TRAMITE)

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en el atributo 'idCaja' de la clase 'Ingresos'.
        """
        return 'Ingreso ' + str(self.idCaja)

class AdquisicionProveedor_Articulos(models.Model):
    idArticulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, help_text='Articulos', verbose_name='Articulo')
    unidades = models.PositiveIntegerField(help_text='Unidades a ingresar', verbose_name='Unidades')
    idAdquisicion = models.ForeignKey(Adquisicion, on_delete=models.CASCADE, help_text='Adquisicion', verbose_name='Adquisicion')

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en los atributos 'idAdquisicion' y 'idArticulo' de la clase 'AdquisicionProveedor_Articulos'.
        """
        return str(self.idAdquisicion) + ' - ' + str(self.idArticulo)

    def _get_subtotal(self):
        return self.unidades * self.idArticulo.precio
    subtotal = property(_get_subtotal)

    def _get_total_unidades(self):
        total = AdquisicionProveedor_Articulos.objects.all().aggregate(Sum('unidades'))['unidades__sum']
        return total
    total_unidades = property(_get_total_unidades)

    def _get_contador(self):
        cont = AdquisicionProveedor_Articulos.objects.all().count()
        return cont
    contador = property(_get_contador)


class AdquisicionProveedor_Piscinas(models.Model):
    idPiscina = models.ForeignKey(Piscinas, on_delete=models.CASCADE, help_text='Piscina', verbose_name='Piscina')
    unidades = models.PositiveIntegerField(help_text='Unidades a ingresar', verbose_name='Unidades')
    idAdquisicion = models.ForeignKey(Adquisicion, on_delete=models.CASCADE, help_text='Adquisicion', verbose_name='Adquisicion')

    def _get_subtotal(self):
        return self.unidades * self.idPiscina.base_dolar
    subtotal = property(_get_subtotal)

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en los atributos 'idAdquisicion' y 'idPiscina' de la clase 'AdquisicionProveedor_Piscinas'.
        """
        return str(self.idAdquisicion) + ' - ' + str(self.idPiscina)

class Pedidos_Articulos(models.Model):
    idPedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, help_text='Pedido', verbose_name='Pedido')
    unidades = models.PositiveIntegerField(help_text='Unidades a ingresar', verbose_name='Unidades')
    idArticulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, help_text='Articulos', verbose_name='Articulos')

    def _get_subtotal(self):
        return self.unidades * self.idArticulo.iva
    subtotal = property(_get_subtotal)

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en los atributos 'idPedido' y 'idArticulo' de la clase 'Pedidos_Articulos'.
        """
        return str(self.idPedido) + ' - ' + str(self.idArticulo)

class Pedidos_Piscinas(models.Model):
    idPedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, help_text='Pedido', verbose_name='Pedido')
    unidades = models.PositiveIntegerField(help_text='Unidades a ingresar', verbose_name='Unidades')
    idPiscina = models.ForeignKey(Piscinas, on_delete=models.CASCADE, help_text='Piscinas', verbose_name='Piscina')

    def __str__(self):
        """Se encarga de convertir el objeto de la clase seleccionada en una cadena.

        Args:
            self (object): Representa la instancia de la clase. Con esta podemos acceder a los atributos y métodos.

        Returns:
            Se retorna mediante su propia instancia de la clase basada en los atributos 'idPedido' y 'idPiscina' de la clase 'Pedidos_Piscinas'.
        """
        return str(self.idPedido) + ' - ' + str(self.idPiscina)

    def _get_subtotal(self):
        return self.unidades * self.idPiscina.total_dolar
    subtotal = property(_get_subtotal)
