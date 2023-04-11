from django import forms

from .models import Piscinas, Categorias, Articulos, Clientes, Direccion_Cliente, \
    Proveedores, Direccion_Proveedor, Empleados, Direccion_Empleado, Pedidos, Obras, Direccion_Obras, \
    Caja, Egresos, Ingresos, AdquisicionProveedor_Articulos, AdquisicionProveedor_Piscinas, Pedidos_Articulos, \
    Pedidos_Piscinas, Adquisicion

# Para inlines
from django.forms import inlineformset_factory
from extra_views import InlineFormSetFactory

# Para autentificación:
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Section - Autentificación
class UserRegisterForm(UserCreationForm):
    """Esta clase se encarga de generar un formulario estándar que no está vinculado a un modelo de base de datos, heredando de
        de la clase forms.Form de Django. En este formulario se envia los campos 'email', 'password1' y 'password2' para
        ser utilizado en el registro de usuario en el sistema

    Args:
        UserCreationForm (object): clase base que se utiliza para crear formularios en una aplicación web. Es una clase que se utiliza
        para definir campos de formulario y validar los datos enviados por el usuario.

    Returns:
        Un formulario de registro en el sistema.
    """
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

# Section - Categorias
class CategoriasForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = "__all__"
        widgets = {
            'categoria': forms.TextInput(attrs={'class': 'form-control'})
        }

# Section - Clientes
class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = '__all__'
        labels = {
            'dni': 'DNI',
            'nombre': 'Nombre y Apellido',
            'telefono': 'Teléfono',
            'email': 'e-Mail',
            'imagen': 'Imagen',
        }

        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DireccionClientesForm(forms.ModelForm):
    class Meta:
        model = Direccion_Cliente
        fields = ['calle', 'barrio', 'ciudad', 'cp', 'provincia',]

        labels = {
            'calle': 'Calle y Nro',
            'barrio': 'Barrio',
            'ciudad': 'Ciudad',
            'cp': 'Codigo Postal',
            'provincia': 'Provincia',
        }

        widgets = {
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'barrio': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'cp': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-select'}),
        }

# Section - Proveedores
class ProveedoresForm(forms.ModelForm):
    class Meta:
        model = Proveedores
        exclude = ['piscina', 'articulo',]
        labels = {
            'cuit': 'CUIT',
            'nombre': 'Nombre y Apellido',
            'telefono': 'Teléfono',
            'email': 'e-Mail',
            'imagen': 'Imagen',
        }

        widgets = {
            'cuit': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DireccionProveedoresForm(forms.ModelForm):
    class Meta:
        model = Direccion_Proveedor
        fields = ['calle', 'barrio', 'ciudad', 'cp', 'provincia',]

        labels = {
            'calle': 'Calle y Nro',
            'barrio': 'Barrio',
            'ciudad': 'Ciudad',
            'cp': 'Codigo Postal',
            'provincia': 'Provincia',
        }

        widgets = {
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'barrio': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'cp': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-select'}),
        }

# Section - Empleados
class EmpleadosForm(forms.ModelForm):
    class Meta:
        model = Empleados
        fields = '__all__'
        labels = {
            'dni': 'D.N.I',
            'nombre': 'Nombre y Apellido',
            'telefono': 'Teléfono',
            'email': 'e-Mail',
            'rol': 'Rol',
            'imagen': 'Imagen',
        }

        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

class DireccionEmpleadosForm(forms.ModelForm):
    class Meta:
        model = Direccion_Empleado
        fields = ['calle', 'barrio', 'ciudad', 'cp', 'provincia',]

        labels = {
            'calle': 'Calle y Nro',
            'barrio': 'Barrio',
            'ciudad': 'Ciudad',
            'cp': 'Codigo Postal',
            'provincia': 'Provincia',
        }

        widgets = {
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'barrio': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'cp': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-select'}),
        }

# Section - Obras
class ObrasForm(forms.ModelForm):
    class Meta:
        model = Obras
        fields = '__all__'
        labels = {
            'fechaInicio': 'Fecha de Inicio:',
            'fechaFinal': 'Fecha de Cierre:',
            'numeroPedido': 'Pedido N°',
            'idEmpleado': 'Empleado',
        }

        widgets = {
            'fechaInicio': forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}),
            'fechaFinal': forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}),
            'numeroPedido': forms.Select(attrs={'class': 'form-select'}),
            'idEmpleado': forms.Select(attrs={'class': 'form-select'}),
        }

class DireccionObrasForm(forms.ModelForm):
    class Meta:
        model = Direccion_Obras
        fields = ['calle', 'barrio', 'ciudad', 'cp', 'provincia',]

        labels = {
            'calle': 'Calle y Nro',
            'barrio': 'Barrio',
            'ciudad': 'Ciudad',
            'cp': 'Codigo Postal',
            'provincia': 'Provincia',
        }

        widgets = {
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'barrio': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'cp': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-select'}),
        }

# Section - Piscinas
class PiscinasForm(forms.ModelForm):
    class Meta:
        model = Piscinas
        exclude = ['pedidosPisc', 'proveedor', 'adquisicionPisc']

        labels = {
            'descripcion': 'Descripcion',
            'unidades': 'Unidades',
            'imagen': 'Imagen',
            'base': 'Base ($)',
            'sf_casilla': 'SF-Casilla ($)',
            'ac': 'AC ($)',
            'al': 'AL ($)',
            'ah': 'AH ($)',
            'mam': 'MAM ($)',
        }

        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'unidades': forms.TextInput(attrs={'class': 'form-control'}),
            'base': forms.TextInput(attrs={'class': 'form-control'}),
            'sf_casilla': forms.TextInput(attrs={'class': 'form-control'}),
            'ac': forms.TextInput(attrs={'class': 'form-control'}),
            'al': forms.TextInput(attrs={'class': 'form-control'}),
            'ah': forms.TextInput(attrs={'class': 'form-control'}),
            'mam': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Section - Articulos
class ArticulosForm(forms.ModelForm):
    class Meta:
        model = Articulos
        exclude =['pedidosArtic', 'proveedor']

        labels = {
            'descripcion': 'Articulo',
            'precio': 'Precio',
            'porcentaje': 'Porcentaje de Rentabilidad',
            'stock': 'Stock',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'categoria': 'Categoria',
            'imagen': 'Imagen',
        }

        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.TextInput(attrs={'class': 'form-control'}),
            'porcentaje': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }

# Section - Adquisiciones
class AdquisicionesForm(forms.ModelForm):
    class Meta:
        model = Adquisicion
        fields = [ 'fechaEntrega', 'fechaRecibido', 'idProveedor', 'estado', 'metodoPago',]

        labels = {
            'idProveedor': 'Proveedor',
            'estado': 'Estado',
            'metodoPago': 'Metodo de Pago',
            'fechaEntrega': 'Fecha de Entrega',
            'fechaRecibido': 'Fecha de Recibido',
        }

        widgets = {
            'idProveedor': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'metodoPago': forms.Select(attrs={'class': 'form-select'}),
            'fechaEntrega': forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}),
            'fechaRecibido': forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}),
        }

class AdquisicionesArticulosForm(forms.ModelForm):
    class Meta:
        model = AdquisicionProveedor_Articulos
        exclude = ['idAdquisicion',]

        labels = {
            'unidades': 'Unidades',
            'idArticulo': 'Articulo',
        }

        widgets = {
            'unidades': forms.TextInput(attrs={'class': 'form-control'}),
            'idArticulo': forms.Select(attrs={'class': 'form-select'}),
        }

class AdquisicionesPiscinasForm(forms.ModelForm):
    class Meta:
        model = AdquisicionProveedor_Piscinas
        exclude = ['idAdquisicion',]

        labels = {
            'unidades': 'Unidades',
            'idPiscina': 'Piscina',
        }

        widgets = {
            'unidades': forms.TextInput(attrs={'class': 'form-control'}),
            'idPiscina': forms.Select(attrs={'class': 'form-select'}),
        }

# Section - Pedidos
class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['fecha', 'idCliente', 'estado', 'metodoPago',]

        labels = {
            'idCliente': 'Cliente',
            'estado': 'Estado',
            'metodoPago': 'Metodo de Pago',
            'fecha': 'Fecha',
        }

        widgets = {
            'idCliente': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'metodoPago': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}),
        }

class PedidosArticulosForm(forms.ModelForm):
    class Meta:
        model = Pedidos_Articulos
        exclude = ['idPedido',]

        labels = {
            'unidades': 'Unidades',
            'idArticulo': 'Articulos',
        }

        widgets = {
            'unidades': forms.TextInput(attrs={'class': 'form-control'}),
            'idArticulo': forms.Select(attrs={'class': 'form-select'}),
        }

class PedidosPiscinasForm(forms.ModelForm):
    class Meta:
        model = Pedidos_Piscinas
        exclude = ['idPedido',]

        labels = {
            'unidades': 'Unidades',
            'idPiscina': 'Piscina',
        }

        widgets = {
            'unidades': forms.TextInput(attrs={'class': 'form-control'}),
            'idPiscina': forms.Select(attrs={'class': 'form-select'}),
        }

# Section - Caja
class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        exclude = ['ingresoCaja', 'egresoCaja',]

        labels = {
            'idEmpleado': 'Empleado',
            'fecha': 'Fecha',
            'tipo': 'Tipo',
        }

        widgets = {
            'idEmpleado': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

class IngresosForm(forms.ModelForm):
    class Meta:
        model = Ingresos
        fields = ['idPedido', 'condicion', 'metodoPago', 'valor']

        labels = {
            'metodoPago': 'Metodo de Pago',
            'valor': 'Valor',
            'idPedido': 'Pedido',
            'condicion': 'Condicion'
        }

        widgets = {
            'idCaja': forms.Select(attrs={'class': 'form-select'}),
            'metodoPago': forms.Select(attrs={'class': 'form-select'}),
            'valor': forms.TextInput(attrs={'class': 'form-control'}),
            'idPedido': forms.Select(attrs={'class': 'form-select'}),
            'condicion': forms.Select(attrs={'class': 'form-select'}),
        }

class EgresosForm(forms.ModelForm):
    class Meta:
        model = Egresos
        fields = ['idAdquisicion', 'condicion', 'metodoPago', 'valor']

        labels = {
            'metodoPago': 'Metodo de Pago',
            'valor': 'Valor',
            'idAdquisicion': 'Adquisicion',
            'condicion': 'Condicion'
        }

        widgets = {
            'metodoPago': forms.Select(attrs={'class': 'form-select'}),
            'valor': forms.TextInput(attrs={'class': 'form-control'}),
            'idAdquisicion': forms.Select(attrs={'class': 'form-select'}),
            'idProveedor': forms.Select(attrs={'class': 'form-select'}),
            'condicion': forms.Select(attrs={'class': 'form-select'}),
        }

class IngresoInline(InlineFormSetFactory):
   model = Ingresos
   form_class = IngresosForm
   factory_kwargs = {'extra': 5, 'max_num': None, 'can_order': False, 'can_delete': False}

class EgresoInline(InlineFormSetFactory):
   model = Egresos
   form_class = EgresosForm
   factory_kwargs = {'extra': 5, 'max_num': None, 'can_order': False, 'can_delete': False}

class Adquisicion_ArticulosInline(InlineFormSetFactory):
   model = AdquisicionProveedor_Articulos
   form_class = AdquisicionesArticulosForm
   factory_kwargs = {'extra': 5, 'max_num': None, 'can_order': False, 'can_delete': False}

class Adquisicion_PiscinasInline(InlineFormSetFactory):
   model = AdquisicionProveedor_Piscinas
   form_class = AdquisicionesPiscinasForm
   factory_kwargs = {'extra': 2, 'max_num': None, 'can_order': False, 'can_delete': False}

class Pedido_ArticulosInline(InlineFormSetFactory):
   model = Pedidos_Articulos
   form_class = PedidosArticulosForm
   factory_kwargs = {'extra': 5, 'max_num': None, 'can_order': False, 'can_delete': False}

class Pedido_PiscinasInline(InlineFormSetFactory):
   model = Pedidos_Piscinas
   form_class = PedidosPiscinasForm
   factory_kwargs = {'extra': 2, 'max_num': None, 'can_order': False, 'can_delete': False}

Adq_ArtFormSet = inlineformset_factory(Adquisicion, AdquisicionProveedor_Articulos,
                                            form=AdquisicionesArticulosForm, extra=15)

Adq_PiscFormSet = inlineformset_factory(Adquisicion, AdquisicionProveedor_Piscinas,
                                            form=AdquisicionesPiscinasForm, extra=3)

Ped_ArtFormSet = inlineformset_factory(Pedidos, Pedidos_Articulos,
                                            form=PedidosArticulosForm, extra=15)

Ped_PiscFormSet = inlineformset_factory(Pedidos, Pedidos_Piscinas,
                                            form=PedidosPiscinasForm, extra=3)

IngresosFormSet = inlineformset_factory(Caja, Ingresos,
                                            form=IngresosForm, extra=20)

EgresosFormSet = inlineformset_factory(Caja, Egresos,
                                            form=EgresosForm, extra=20)