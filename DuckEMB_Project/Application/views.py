from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.views.generic import DetailView, CreateView, TemplateView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from .models import Piscinas, Categorias, Articulos, Clientes, Direccion_Cliente, \
   Proveedores, Direccion_Proveedor, Empleados, Direccion_Empleado, Pedidos, Obras, Direccion_Obras, \
   Caja, Egresos, Ingresos, AdquisicionProveedor_Articulos, AdquisicionProveedor_Piscinas, Pedidos_Articulos, \
   Pedidos_Piscinas, Adquisicion, Metodos_Pagos
from .forms import CategoriasForm, ClientesForm, DireccionClientesForm, ProveedoresForm, DireccionProveedoresForm, \
   EmpleadosForm, DireccionEmpleadosForm, ObrasForm, DireccionObrasForm, PiscinasForm, \
   ArticulosForm, AdquisicionesArticulosForm, AdquisicionesPiscinasForm, PedidosPiscinasForm, PedidosArticulosForm, \
   AdquisicionesForm, PedidosForm, CajaForm, EgresosForm, IngresosForm, Adq_ArtFormSet, Adq_PiscFormSet, Ped_ArtFormSet, \
   Ped_PiscFormSet, EgresosFormSet, IngresosFormSet, IngresoInline, EgresoInline, Adquisicion_ArticulosInline, \
   Adquisicion_PiscinasInline, Pedido_ArticulosInline, Pedido_PiscinasInline

# Para impresion
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Para permisos
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

# Para autentificación:
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

# Para inlines
from extra_views import  UpdateWithInlinesView, NamedFormsetsMixin

#Para renderizar el mail de recupero de contraseña:
from django.contrib.auth.views import PasswordResetView
from django.utils.html import strip_tags
from django.views.generic import FormView
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django import template
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

# Create your views here.

def index(request):
   user = User.objects.all()
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   return render(request, 'base.html', {'formato': formato, "user": user})

@login_required
def vHome(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   caja = Caja.objects.all()
   ingresos = Ingresos.objects.all()
   egresos = Egresos.objects.all()
   data = Piscinas.objects.all()
   clientes = Clientes.objects.count()
   context = {'caja': caja, 'ingresos': ingresos, 'egresos': egresos, 'data': data, 'formato': formato, 'clientes': clientes}
   return render(request, 'home.html', context)

@login_required
def terminos(request):
   """Esta función se encarga de renderizar la página de terminos y condiciones del sistema entregandoles los argumentos a la plantilla 'terminos.html'.

   Args:
      request (object): Sirve para entregar los objetos que contienen los metadatos de la solicitud que van a ser enviado a la plantilla.

   Returns:
      Se renderiza la página con los argumentos pasados en la plantilla 'terminos.html'
    """
   return render(request, 'terminos.html')

# Vistas de Autentificación
def registerPage(request):

   if request.method == 'POST':
      form = UserRegisterForm(request.POST)
      if form.is_valid():
         form.save()
         username = form.cleaned_data['username']
         messages.success(request, f'Usuario {username} creado')
         return redirect("/login")
      else:
         messages.error(request, 'Incorrecto')

   else:
      form = UserRegisterForm()

   context = {'form': form}
   return render(request, 'registration/register.html', context)

# Vistas de Autentificación
class SuccessMessageMixin:
   success_message = ''

   def form_valid(self, form):
      response = super().form_valid(form)
      success_message = self.get_success_message(form.cleaned_data)
      if success_message:
         messages.success(self.request, success_message)
      return response

   def get_success_message(self, cleaned_data):
      return self.success_message % cleaned_data

# Handler_Error
class Error400View(TemplateView):
   template_name = "error_400.html"

class Error403View(TemplateView):
   template_name = "error_403.html"

class Error404View(TemplateView):
   template_name = "error_404.html"

class Error500View(TemplateView):
   template_name = "error_500.html"

   @classmethod
   def as_error_view(cls):

      v = cls.as_view()
      def view(request):
         r = v(request)
         r.render()
         return r
      return view

# Para provocar error 500.
class VistaEjemplo(TemplateView):
   template_name = "ejemplo.html"

   def get_context_data(self, **kwargs):
      context = super(VistaEjemplo, self).get_context_data(**kwargs)
      a = 'prueba'
      print(a/10)
      return context

# Section - Categorias
@login_required
def Categoria(request):
   categoria = Categorias.objects.all()
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   context = {'categoria': categoria, 'formato': formato}
   return render(request, 'Categorias/categorias.html', context)

class NewCategoriaView(SuccessMessageMixin, PermissionRequiredMixin, FormView):
   permission_required = 'Application.add_categorias'
   template_name = 'Categorias/categoria-form.html'
   form_class = CategoriasForm
   success_url = "/categorias"
   success_message = "Se ha añadido con éxito la nueva categoria."

   def form_valid(self, form):
      form.save()
      return super().form_valid(form)

class ModCategoriaView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
   permission_required = 'Application.change_categorias'
   model = Categorias
   form_class = CategoriasForm
   template_name = 'Categorias/categoria-form.html'
   success_url = "/categorias"
   success_message = "Se ha actualizado con éxito la categoria seleccionada."

class DeleteCategoriaView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_categorias'
   model = Categorias
   template_name = 'Categorias/categoria-delete-form.html'
   success_url = "/categorias"
   success_message = "Se ha eliminado con éxito la categoria seleccionada."

@login_required
def ArticulosxCategoria(request, pk):
   categoria = Categorias.objects.filter(id=pk)
   articulos = Articulos.objects.all()
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   return render(request, 'Categorias/articulosxcategoria.html', {'articulos': articulos, 'categoria': categoria, 'formato': formato})

# Section - Clientes
@login_required
def vClienteDireccion(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   cliente = Clientes.objects.all()
   direccion = Direccion_Cliente.objects.all()
   context = {'cliente': cliente, 'direccion': direccion, 'formato': formato}
   return render(request, 'Clientes/clientes.html', context)

class CreateCliente(CreateView):
   model = Direccion_Cliente
   template_name = 'Clientes/clientes-form.html'
   form_class = DireccionClientesForm
   second_form_class = ClientesForm
   success_url = "/clientes"

   def get_context_data(self, **kwargs):
      context = super(CreateCliente, self).get_context_data(**kwargs)
      if 'form' not in context:
         context['form'] = self.form_class(self.request.GET)
      if 'form2' not in context:
         context['form2'] = self.second_form_class(self.request.GET)
      return context

   def post(self, request, *args, **kwargs):
      self.object = self.get_object
      form = self.form_class(request.POST)
      form2 = self.second_form_class(request.POST)

      if form.is_valid() and form2.is_valid():
         direc = form.save(commit=False)
         direc.idCliente = form2.save()
         direc.save()
         messages.success(request, 'Se ha añadido con éxito un nuevo cliente.')
         return HttpResponseRedirect(self.get_success_url())
      else:
         return self.render_to_response(self.get_context_data(form=form, form2=form2))

class UpdateCliente(UpdateView):
   model = Direccion_Cliente
   second_model = Clientes
   template_name = 'Clientes/clientes-form.html'
   form_class = DireccionClientesForm
   second_form_class = ClientesForm
   success_url = "/clientes"
   
   def get_context_data(self, **kwargs):
      context = super(UpdateCliente, self).get_context_data(**kwargs)
      pk = self.kwargs.get('pk', 0)
      direccion = self.model.objects.get(id=pk)
      cliente = self.second_model.objects.get(dni = direccion.idCliente_id)
      if 'form' not in context:
         context['form'] = self.form_class(self.request.GET)
      if 'form2' not in context:
         context['form2'] = self.second_form_class(instance=cliente)
      context['id'] = pk
      return context
   
   def post(self, request, *args, **kwargs):
         self.object = self.get_object
         id_direccion = kwargs['pk']
         direccion = self.model.objects.get(id=id_direccion)
         cliente = self.second_model.objects.get(dni = direccion.idCliente_id)
         form = self.form_class(request.POST, instance= direccion)
         form2 = self.second_form_class(request.POST, instance= cliente)

         if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            messages.success(request, 'Se ha actualizado con éxito el cliente seleccionado.')
            return HttpResponseRedirect(self.get_success_url())
         else:
            return HttpResponseRedirect(self.get_success_url())

class DeleteClienteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_clientes'
   model = Clientes
   template_name = 'Clientes/clientes-delete-form.html'
   success_url = "/clientes"
   success_message = "Se ha eliminado con éxito el cliente seleccionado."

@login_required
def PedidoxCliente(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   cliente = Clientes.objects.filter(dni=pk)
   pedido = Pedidos.objects.all()
   return render(request, 'Clientes/pedidoxcliente.html', {'pedido': pedido, 'cliente': cliente, 'formato': formato})

# Section - Proveedor
@login_required
@permission_required('is_superuser')
def vProveedorDireccion(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   proveedor = Proveedores.objects.all()
   direccion = Direccion_Proveedor.objects.all()
   context = {'proveedor': proveedor, 'direccion': direccion, 'formato': formato}
   return render(request, 'Proveedores/proveedores.html', context)

class CreateProveedor(PermissionRequiredMixin, CreateView):
   permission_required = 'Application.add_proveedores'
   model = Direccion_Proveedor
   template_name = 'Proveedores/proveedores-form.html'
   form_class = DireccionProveedoresForm
   second_form_class = ProveedoresForm
   success_url = "/proveedores"

   def get_context_data(self, **kwargs):
      context = super(CreateProveedor, self).get_context_data(**kwargs)
      if 'form' not in context:
         context['form'] = self.form_class(self.request.GET)
      if 'form2' not in context:
         context['form2'] = self.second_form_class(self.request.GET)
      return context

   def post(self, request, *args, **kwargs):
      self.object = self.get_object
      form = self.form_class(request.POST)
      form2 = self.second_form_class(request.POST)

      if form.is_valid() and form2.is_valid():
         direc = form.save(commit=False)
         direc.idProveedor = form2.save()
         direc.save()
         messages.success(request, 'Se ha añadido con éxito un nuevo proveedor.')
         return HttpResponseRedirect(self.get_success_url())
      else:
         return self.render_to_response(self.get_context_data(form=form, form2=form2))

class UpdateProveedor(UpdateView):
   model = Direccion_Proveedor
   second_model = Proveedores
   template_name = 'Proveedores/proveedores-form.html'
   form_class = DireccionProveedoresForm
   second_form_class = ProveedoresForm
   success_url = "/proveedores"
   
   def get_context_data(self, **kwargs):
      context = super(UpdateProveedor, self).get_context_data(**kwargs)
      pk = self.kwargs.get('pk', 0)
      direccion = self.model.objects.get(id=pk)
      proveedor = self.second_model.objects.get(cuit = direccion.idProveedor_id)
      if 'form' not in context:
         context['form'] = self.form_class(self.request.GET)
      if 'form2' not in context:
         context['form2'] = self.second_form_class(instance=proveedor)
      context['id'] = pk
      return context
   
   def post(self, request, *args, **kwargs):
         self.object = self.get_object
         id_direccion = kwargs['pk']
         direccion = self.model.objects.get(id=id_direccion)
         proveedor = self.second_model.objects.get(cuit = direccion.idProveedor_id)
         form = self.form_class(request.POST, instance= direccion)
         form2 = self.second_form_class(request.POST, instance=proveedor)

         if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            messages.success(request, 'Se ha actualizado con éxito el proveedor seleccionado.')
            return HttpResponseRedirect(self.get_success_url())
         else:
            return HttpResponseRedirect(self.get_success_url())

class DeleteProveedorView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_proveedores'
   model = Proveedores
   template_name = 'Proveedores/proveedores-delete-form.html'
   success_url = "/proveedores"
   success_message = "Se ha eliminado con éxito el proveedor seleccionado."

@login_required
def AdquisiciónxProveedor(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   proveedor = Proveedores.objects.filter(cuit=pk)
   adquisicion = Adquisicion.objects.all()
   return render(request, 'Proveedores/adquisiciónxproveedor.html', {'adquisicion': adquisicion, 'proveedor': proveedor, 'formato': formato})

# Section - Empleado
@login_required
@permission_required('is_superuser')
def vEmpleadoDireccion(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   empleado = Empleados.objects.all()
   direccion = Direccion_Empleado.objects.all()
   context = {'empleado': empleado, 'direccion': direccion, 'formato': formato}
   return render(request, 'Empleados/empleados.html', context)

class CreateEmpleado(PermissionRequiredMixin, CreateView):
   permission_required = 'Application.add_empleados'
   model = Direccion_Empleado
   template_name = 'Empleados/empleados-form.html'
   form_class = DireccionEmpleadosForm
   second_form_class = EmpleadosForm
   success_url = "/empleados"

   def get_context_data(self, **kwargs):
      context = super(CreateEmpleado, self).get_context_data(**kwargs)
      if 'form' not in context:
         context['form'] = self.form_class(self.request.GET)
      if 'form2' not in context:
         context['form2'] = self.second_form_class(self.request.GET)
      return context

   def post(self, request, *args, **kwargs):
      self.object = self.get_object
      form = self.form_class(request.POST)
      form2 = self.second_form_class(request.POST)

      if form.is_valid() and form2.is_valid():
         direc = form.save(commit=False)
         direc.idEmpleado = form2.save()
         direc.save()
         messages.success(request, 'Se ha añadido con éxito un nuevo empleado.')
         return HttpResponseRedirect(self.get_success_url())
      else:
         return self.render_to_response(self.get_context_data(form=form, form2=form2))

class UpdateEmpleado(UpdateView):
   model = Direccion_Empleado
   second_model = Empleados
   template_name = 'Empleados/empleados-form.html'
   form_class = DireccionEmpleadosForm
   second_form_class = EmpleadosForm
   success_url = "/empleados"
   
   def get_context_data(self, **kwargs):
      context = super(UpdateEmpleado, self).get_context_data(**kwargs)
      pk = self.kwargs.get('pk', 0)
      direccion = self.model.objects.get(id=pk)
      empleado = self.second_model.objects.get(dni = direccion.idEmpleado_id)
      if 'form' not in context:
         context['form'] = self.form_class(self.request.GET)
      if 'form2' not in context:
         context['form2'] = self.second_form_class(instance=empleado)
      context['id'] = pk
      return context
   
   def post(self, request, *args, **kwargs):
         self.object = self.get_object
         id_direccion = kwargs['pk']
         direccion = self.model.objects.get(id=id_direccion)
         empleado = self.second_model.objects.get(dni = direccion.idEmpleado_id)
         form = self.form_class(request.POST, instance= direccion)
         form2 = self.second_form_class(request.POST, instance= empleado)

         if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            messages.success(request, 'Se ha actualizado con éxito el empleado seleccionado.')
            return HttpResponseRedirect(self.get_success_url())
         else:
            return HttpResponseRedirect(self.get_success_url())

class DeleteEmpleadoView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_empleados'
   model = Empleados
   template_name = 'Empleados/empleados-delete-form.html'
   success_url = "/empleados"
   success_message = "Se ha eliminado con éxito el empleado seleccionado."

@login_required
def Empleado_AD(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   empleado = Empleados.objects.filter(rol='AD')
   direccion = Direccion_Empleado.objects.all()
   return render(request, 'Empleados/empleado_ad.html', {'empleado': empleado, 'direccion': direccion, 'formato': formato})

@login_required
def Empleado_OB(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   empleado = Empleados.objects.filter(rol='OB')
   direccion = Direccion_Empleado.objects.all()
   return render(request, 'Empleados/empleado_ob.html', {'empleado': empleado, 'direccion': direccion, 'formato': formato})

@login_required
def Empleado_TE(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   empleado = Empleados.objects.filter(rol='TE')
   direccion = Direccion_Empleado.objects.all()
   return render(request, 'Empleados/empleado_te.html', {'empleado': empleado, 'direccion': direccion, 'formato': formato})

@login_required
def Empleado_GE(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   empleado = Empleados.objects.filter(rol='GE')
   direccion = Direccion_Empleado.objects.all()
   return render(request, 'Empleados/empleado_ge.html', {'empleado': empleado, 'direccion': direccion, 'formato': formato})

@login_required
def Empleado_VE(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   empleado = Empleados.objects.filter(rol='VE')
   direccion = Direccion_Empleado.objects.all()
   return render(request, 'Empleados/empleado_ve.html', {'empleado': empleado, 'direccion': direccion, 'formato': formato})

@login_required
def Empleado_LO(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   empleado = Empleados.objects.filter(rol='LO')
   direccion = Direccion_Empleado.objects.all()
   return render(request, 'Empleados/empleado_lo.html', {'empleado': empleado, 'direccion': direccion, 'formato': formato})

@login_required
def CajaxEmpleado(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   empleado = Empleados.objects.filter(dni=pk)
   caja = Caja.objects.all()
   return render(request, 'Empleados/cajaxempleado.html', {'caja': caja, 'empleado': empleado, 'formato': formato})

# Section - Obras
@login_required
def vObraDireccion(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   obra = Obras.objects.all()
   direccion = Direccion_Obras.objects.all()
   context = {'obra': obra, 'direccion': direccion, 'formato': formato}
   return render(request, 'Obras/obras.html', context)

class CreateObra(CreateView):
   model = Direccion_Obras
   template_name = 'Obras/obras-form.html'
   form_class = DireccionObrasForm
   second_form_class = ObrasForm
   success_url = "/obras"

   def get_context_data(self, **kwargs):
      context = super(CreateObra, self).get_context_data(**kwargs)
      if 'form' not in context:
         context['form'] = self.form_class(self.request.GET)
      if 'form2' not in context:
         context['form2'] = self.second_form_class(self.request.GET)
      return context

   def post(self, request, *args, **kwargs):
      self.object = self.get_object
      form = self.form_class(request.POST)
      form2 = self.second_form_class(request.POST)

      if form.is_valid() and form2.is_valid():
         direc = form.save(commit=False)
         direc.idObra = form2.save()
         direc.save()
         messages.success(request, 'Se ha añadido con éxito una nueva obra.')
         return HttpResponseRedirect(self.get_success_url())
      else:
         return self.render_to_response(self.get_context_data(form=form, form2=form2))

class UpdateObra(UpdateView):
   model = Direccion_Obras
   second_model = Obras
   template_name = 'Obras/obras-form.html'
   form_class = DireccionObrasForm
   second_form_class = ObrasForm
   success_url = "/obras"
   
   def get_context_data(self, **kwargs):
      context = super(UpdateObra, self).get_context_data(**kwargs)
      pk = self.kwargs.get('pk', 0)
      direccion = self.model.objects.get(id=pk)
      obra = self.second_model.objects.get(id = direccion.idObra_id)
      if 'form' not in context:
         context['form'] = self.form_class(self.request.GET)
      if 'form2' not in context:
         context['form2'] = self.second_form_class(instance=obra)
      context['id'] = pk
      return context
   
   def post(self, request, *args, **kwargs):
         self.object = self.get_object
         id_direccion = kwargs['pk']
         direccion = self.model.objects.get(id=id_direccion)
         obra = self.second_model.objects.get(id = direccion.idObra_id)
         form = self.form_class(request.POST, instance= direccion)
         form2 = self.second_form_class(request.POST, instance= obra)

         if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            messages.success(request, 'Se ha actualizado con éxito la obra seleccionada.')
            return HttpResponseRedirect(self.get_success_url())
         else:
            return HttpResponseRedirect(self.get_success_url())

class DeleteObraView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_obras'
   model = Obras
   template_name = 'Obras/obras-delete-form.html'
   success_url = "/obras"
   success_message = "Se ha eliminado con éxito la obra seleccionada."

# Section - Piscinas
@login_required
def vPiscinas(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   piscina = Piscinas.objects.all()
   context = {'piscina': piscina, 'formato': formato}
   return render(request, 'Piscinas/piscinas.html', context)

class NewPiscinaView(SuccessMessageMixin, FormView):
   template_name = 'Piscinas/piscinas-form.html'
   form_class = PiscinasForm
   success_url = "/piscinas"
   success_message = "Se ha añadido con éxito la nueva piscina."

   def form_valid(self, form):
       form.save()
       return super().form_valid(form)

class ModPiscinaView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
   permission_required = 'Application.change_piscinas'
   model = Piscinas
   form_class = PiscinasForm
   template_name = 'Piscinas/piscinas-form.html'
   success_url = "/piscinas"
   success_message = "Se ha actualizado con éxito la piscina seleccionada."

class DeletePiscinaView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_piscinas'
   model = Piscinas
   template_name = 'Piscinas/piscinas-delete-form.html'
   success_url = "/piscinas"
   success_message = "Se ha eliminado con éxito la piscina seleccionada."

@login_required
def DetailPiscina(request, pk):
   data = Piscinas.objects.filter(id=pk)
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   context = {
      'data': data,
      'formato': formato,
   }
   return render(request, 'Piscinas/detail-piscinas.html', context)

@login_required
def AdquisicionxPiscinas(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   prod = Piscinas.objects.filter(id=pk)
   piscinas = AdquisicionProveedor_Piscinas.objects.filter(idPiscina_id=pk)
   return render(request, 'Piscinas/adquisicionxpiscinas.html', {'piscinas': piscinas, 'prod': prod, 'formato': formato})

@login_required
def PedidoxPiscinas(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   prod = Piscinas.objects.filter(id=pk)
   piscinas = Pedidos_Piscinas.objects.filter(idPiscina_id=pk)
   return render(request, 'Piscinas/pedidoxpiscinas.html', {'piscinas': piscinas, 'prod': prod, 'formato': formato})

# Section - Articulos
@login_required
def vArticulos(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   articulo = Articulos.objects.all()
   context = {'articulo': articulo, 'formato': formato}
   return render(request, 'Articulos/articulos.html', context)

class NewArticuloView(SuccessMessageMixin, FormView):
   template_name = 'Articulos/articulos-form.html'
   form_class = ArticulosForm
   success_url = "/articulos"
   success_message = "Se ha añadido con éxito el nuevo articulo."

   def form_valid(self, form):
       form.save()
       return super().form_valid(form)

class ModArticuloView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
   permission_required = 'Application.change_articulos'
   model = Articulos
   form_class = ArticulosForm
   template_name = 'Articulos/articulos-form.html'
   success_url = "/articulos"
   success_message = "Se ha modificado con éxito el articulo solicitado."

class DeleteArticuloView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_articulos'
   model = Articulos
   template_name = 'Articulos/articulos-delete-form.html'
   success_url = "/articulos"
   success_message = "Se ha eliminado con éxito el articulo solicitado."

class DetailArticuloView(DetailView):
   model = Articulos
   template_name = 'Articulos/articulos-detail-form.html'

@login_required
def AdquisicionxArticulos(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   prod = Articulos.objects.filter(id=pk)
   articulos = AdquisicionProveedor_Articulos.objects.filter(idArticulo_id=pk)
   return render(request, 'Articulos/adquisicionxarticulos.html', {'articulos': articulos, 'prod': prod, 'formato': formato})

@login_required
def PedidoxArticulos(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   prod = Articulos.objects.filter(id=pk)
   articulos = Pedidos_Articulos.objects.filter(idArticulo_id=pk)
   return render(request, 'Articulos/pedidoxarticulos.html', {'articulos': articulos, 'prod': prod, 'formato': formato})

# Section - Adquisicion
@login_required
def vAdquisicion(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   adquisicion = Adquisicion.objects.all()
   articulos = AdquisicionProveedor_Articulos.objects.all()
   piscinas = AdquisicionProveedor_Piscinas.objects.all()
   context = {'adquisicion': adquisicion, 'articulos': articulos, 'piscinas': piscinas, 'formato': formato}
   return render(request, 'Adquisicion/adquisiciones.html', context)

@login_required
def Historico_Adquisiciones(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   adquisicion = Adquisicion.objects.all()
   articulos = AdquisicionProveedor_Articulos.objects.all()
   piscinas = AdquisicionProveedor_Piscinas.objects.all()
   context = {'adquisicion': adquisicion, 'articulos': articulos, 'piscinas': piscinas, 'formato': formato}
   return render(request, 'Adquisicion/historico_adquisiciones.html', context)

@login_required
def vAdquisicion_Articulos(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   adquisicion = Adquisicion.objects.all()
   articulos = AdquisicionProveedor_Articulos.objects.all()
   context = {'adquisicion': adquisicion, 'articulos': articulos, 'formato': formato}
   return render(request, 'Adquisicion/adquisiciones_articulos.html', context)

@login_required
def vAdquisicion_Piscinas(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   adquisicion = Adquisicion.objects.all()
   piscinas = AdquisicionProveedor_Piscinas.objects.all()
   context = {'adquisicion': adquisicion, 'piscinas': piscinas, 'formato': formato}
   return render(request, 'Adquisicion/adquisiciones_piscinas.html', context)

class ModAdquisicionView(PermissionRequiredMixin, UpdateView):
   permission_required = 'Application.change_adquisicion'
   model = Adquisicion
   form_class = AdquisicionesForm
   template_name = 'Adquisicion/adquisiciones-form.html'
   success_url = "/adquisiciones"

class ModAdqArticulosView(PermissionRequiredMixin, UpdateView):
   permission_required = 'Application.change_adquisicionproveedor_articulos'
   model = AdquisicionProveedor_Articulos
   form_class = AdquisicionesArticulosForm
   template_name = 'Adquisicion/adqarticulos-form.html'
   success_url = "/adquisicionesArt"

class ModAdqPiscinasView(PermissionRequiredMixin, UpdateView):
   permission_required = 'Application.change_adquisicionproveedor_piscinas'
   model = AdquisicionProveedor_Piscinas
   form_class = AdquisicionesPiscinasForm
   template_name = 'Adquisicion/adqpiscinas-form.html'
   success_url = "/adquisicionesPisc"

class DeleteAdquisicionView(PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_adquisicion'
   model = Adquisicion
   template_name = 'Adquisicion/adquisicion-delete-form.html'
   success_url = "/adquisiciones"

class DeleteAdqArticuloView(PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_adquisicionproveedor_articulos'
   model = AdquisicionProveedor_Articulos
   template_name = 'Adquisicion/adqArticulos-delete-form.html'
   success_url = "/adquisicionesArt"

class DeleteAdqPiscinaView(PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_adquisicionproveedor_piscinas'
   model = AdquisicionProveedor_Piscinas
   template_name = 'Adquisicion/adqPiscinas-delete-form.html'
   success_url = "/adquisicionesPisc"

@login_required
def Adquisicion_PR(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   adquisicion = Adquisicion.objects.filter(estado='PR')
   return render(request, 'Adquisicion/adquisicion_pr.html', {'adquisicion': adquisicion, 'formato': formato})

@login_required
def Adquisicion_AR(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   adquisicion = Adquisicion.objects.filter(estado='AR')
   return render(request, 'Adquisicion/adquisicion_ar.html', {'adquisicion': adquisicion, 'formato': formato})

@login_required
def Adquisicion_EN(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   adquisicion = Adquisicion.objects.filter(estado='EN')
   return render(request, 'Adquisicion/adquisicion_en.html', {'adquisicion': adquisicion, 'formato': formato})

@login_required
def Adquisicion_DE(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   adquisicion = Adquisicion.objects.filter(estado='DE')
   return render(request, 'Adquisicion/adquisicion_de.html', {'adquisicion': adquisicion, 'formato': formato})

@login_required
def Adquisicion_CA(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   adquisicion = Adquisicion.objects.filter(estado='CA')
   return render(request, 'Adquisicion/adquisicion_ca.html', {'adquisicion': adquisicion, 'formato': formato})

def AdquisicionxTotalForm(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   adqui = Adquisicion.objects.filter(id = pk)
   articulo = AdquisicionProveedor_Articulos.objects.filter(idAdquisicion=pk)
   precio = Articulos.objects.all()
   piscina = AdquisicionProveedor_Piscinas.objects.filter(idAdquisicion=pk)
   pisc = Piscinas.objects.all()
   return render(request, 'Adquisicion/adq-total.html', {'adqui': adqui, 'articulo': articulo, 'precio': precio, 'piscina': piscina, 'pisc': pisc, 'formato': formato})

@permission_required('is_staff')
def AdquisicionxArticuloForm(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   adqui = Adquisicion.objects.filter(id = pk)
   articulo = AdquisicionProveedor_Articulos.objects.filter(idAdquisicion=pk)
   precio = Articulos.objects.all()
   return render(request, 'Adquisicion/adq-art.html', {'adqui': adqui, 'articulo': articulo, 'precio': precio, 'formato': formato})

@permission_required('is_staff')
def AdquisicionxPiscinaForm(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   adqui = Adquisicion.objects.filter(id = pk)
   piscina = AdquisicionProveedor_Piscinas.objects.filter(idAdquisicion=pk)
   pisc = Piscinas.objects.all()
   return render(request, 'Adquisicion/adq-pisc.html', {'adqui': adqui, 'piscina': piscina, 'pisc': pisc, 'formato': formato})

@login_required
def AdquisicionxMetodoPago(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   pago = Metodos_Pagos.objects.filter(id=pk)
   adquisicion = Adquisicion.objects.filter(metodoPago_id=pk)
   return render(request, 'Adquisicion/adquisicionxpago.html', {'adquisicion': adquisicion, 'pago': pago, 'formato': formato})

class AdquisicionCreateView(CreateView):
   form_class = AdquisicionesForm
   template_name = 'Adquisicion/adqui_form_create.html'
   success_url= '/adquisiciones'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      if self.request.POST:
         context['form'] = AdquisicionesForm(self.request.POST)
         context['formset'] = Adq_ArtFormSet(self.request.POST)
         context['formset2'] = Adq_PiscFormSet(self.request.POST)
      else:
         context['form'] = AdquisicionesForm()
         context['formset'] = Adq_ArtFormSet()
         context['formset2'] = Adq_PiscFormSet()
      return context

   def form_valid(self, form):
      context = self.get_context_data()
      form = context['form']
      formset = context['formset']
      formset2 = context['formset2']
      if form.is_valid() and formset.is_valid() and formset2.is_valid():
         self.object = form.save()
         form.instance = self.object
         form.save()
         formset.instance = self.object
         formset.save()
         formset2.instance = self.object
         formset2.save()
         return super().form_valid(form)
      else:
         return self.render_to_response(self.get_context_data(form=form))

class UpdateAdquisicionView(NamedFormsetsMixin, UpdateWithInlinesView):
   model = Adquisicion
   form_class = AdquisicionesForm
   inlines = [Adquisicion_ArticulosInline, Adquisicion_PiscinasInline]
   inlines_names = ['Articulos', 'Piscinas']
   template_name = 'Adquisicion/adqui_form_update.html'
   success_url= '/adquisiciones'

class Adqui_ArtCreateView(PermissionRequiredMixin, CreateView):
   permission_required = 'Application.add_adquisicionproveedor_articulos'
   form_class = AdquisicionesForm
   template_name = 'Adquisicion/adquiart_form_create.html'

   def get_context_data(self, **kwargs):
      context = super(Adqui_ArtCreateView, self).get_context_data(**kwargs)
      context['adq_art_formset'] = Adq_ArtFormSet()
      return context

   def post(self, request, *args, **kwargs):
      self.object = None
      form_class = self.get_form_class()
      form = self.get_form(form_class)
      adq_art_formset = Adq_ArtFormSet(self.request.POST)
      if form.is_valid() and adq_art_formset.is_valid():
         return self.form_valid(form, adq_art_formset)
      else:
         return self.form_invalid(form, adq_art_formset)

   def form_valid(self, form, adq_art_formset):
      self.object = form.save(commit=False)
      self.object.save()
      # saving ProductMeta Instances
      product_metas = adq_art_formset.save(commit=False)
      for form2 in product_metas:
         form2.idAdquisicion = self.object
         form2.save()
         Art = Articulos.objects.get(id=form2.idArticulo_id)
         Art.stock += form2.unidades
         Art.save()
      return redirect('/adquisiciones')

   def form_invalid(self, form, adq_art_formset):
      return self.render_to_response(
         self.get_context_data(form=form,
                                 adq_art_formset=adq_art_formset
                                 )
      )

class Adqui_PiscCreateView(PermissionRequiredMixin, CreateView):
   permission_required = 'Application.add_adquisicionproveedor_piscinas'
   form_class = AdquisicionesForm
   template_name = 'Adquisicion/adquipisc_form_create.html'

   def get_context_data(self, **kwargs):
      context = super(Adqui_PiscCreateView, self).get_context_data(**kwargs)
      context['adq_Pisc_formset'] = Adq_PiscFormSet()
      return context

   def post(self, request, *args, **kwargs):
      self.object = None
      form_class = self.get_form_class()
      form = self.get_form(form_class)
      adq_Pisc_formset = Adq_PiscFormSet(self.request.POST)
      if form.is_valid() and adq_Pisc_formset.is_valid():
         return self.form_valid(form, adq_Pisc_formset)
      else:
         return self.form_invalid(form, adq_Pisc_formset)

   def form_valid(self, form, adq_Pisc_formset):
      self.object = form.save(commit=False)
      self.object.save()
      # saving ProductMeta Instances
      product_metas = adq_Pisc_formset.save(commit=False)
      for form2 in product_metas:
         form2.idAdquisicion = self.object
         form2.save()
         Pisc = Piscinas.objects.get(id=form2.idPiscina_id)
         Pisc.unidades += form2.unidades
         Pisc.save()

      return redirect('/adquisiciones')

   def form_invalid(self, form, adq_Pisc_formset):
      return self.render_to_response(
         self.get_context_data(form=form,
                                 adq_Pisc_formset=adq_Pisc_formset
                                 )
      )

# Section - Pedidos
@login_required
def vPedidos(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   pedido = Pedidos.objects.all()
   articulos = Pedidos_Articulos.objects.all()
   piscinas = Pedidos_Piscinas.objects.all()
   context = {'pedido': pedido, 'articulos': articulos, 'piscinas': piscinas, 'formato': formato}
   return render(request, 'Pedidos/pedidos.html', context)

@login_required
def Historico_Pedidos(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   pedido = Pedidos.objects.all()
   articulos = Pedidos_Articulos.objects.all()
   piscinas = Pedidos_Piscinas.objects.all()
   context = {'pedido': pedido, 'articulos': articulos, 'piscinas': piscinas, 'formato': formato}
   return render(request, 'Pedidos/historico-pedidos.html', context)

@login_required
def vPedidos_Articulos(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   pedido = Pedidos.objects.all()
   articulos = Pedidos_Articulos.objects.all()
   context = {'pedido': pedido, 'articulos': articulos, 'formato': formato}
   return render(request, 'Pedidos/pedidos_articulos.html', context)

@login_required
def vPedidos_Piscinas(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   pedido = Pedidos.objects.all()
   piscinas = Pedidos_Piscinas.objects.all()
   context = {'pedido': pedido, 'piscinas': piscinas, 'formato': formato}
   return render(request, 'Pedidos/pedidos_piscinas.html', context)

class ModPedidoView(PermissionRequiredMixin, UpdateView):
   permission_required = 'Application.change_pedidos'
   model = Pedidos
   form_class = PedidosForm
   template_name = 'Pedidos/pedidos-form.html'
   success_url = "/pedidos"

class ModPedidoArticulosView(PermissionRequiredMixin, UpdateView):
   permission_required = 'Application.change_pedidos_articulos'
   model = Pedidos_Articulos
   form_class = PedidosArticulosForm
   template_name = 'Pedidos/pedidoarticulos-form.html'
   success_url = "/pedidosArt"

class ModPedidoPiscinasView(PermissionRequiredMixin, UpdateView):
   permission_required = 'Application.change_pedidos_piscinas'
   model = Pedidos_Piscinas
   form_class = PedidosPiscinasForm
   template_name = 'Pedidos/pedidopiscinas-form.html'
   success_url = "/pedidosPisc"

class DeletePedidoView(PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_pedidos'
   model = Pedidos
   template_name = 'Pedidos/pedidos-delete-form.html'
   success_url = "/pedidos"

class DeletePedidoArticulosView(PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_pedidos_articulos'
   model = Pedidos_Articulos
   template_name = 'Pedidos/pedidoarticulos-delete-form.html'
   success_url = "/pedidosArt"

class DeletePedidoPiscinasView(PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_pedidos_piscinas'
   model = Pedidos_Piscinas
   template_name = 'Pedidos/pedidopiscinas-delete-form.html'
   success_url = "/pedidosPisc"

@login_required
def PedidoxTotalForm(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   pedido = Pedidos.objects.filter(id = pk)
   articulo = Pedidos_Articulos.objects.filter(idPedido=pk)
   precio = Articulos.objects.all()
   piscina = Pedidos_Piscinas.objects.filter(idPedido=pk)
   pisc = Piscinas.objects.all()
   return render(request, 'Pedidos/ped-total.html', {'pedido': pedido, 'articulo': articulo, 'precio': precio, 'piscina': piscina, 'pisc': pisc, 'formato': formato})

@login_required
def PedidoxMetodoPago(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   pago = Metodos_Pagos.objects.filter(id=pk)
   pedido = Pedidos.objects.filter(metodoPago_id=pk)
   return render(request, 'Pedidos/pedidoxpago.html', {'pedido': pedido, 'pago': pago, 'formato': formato})

@permission_required('is_staff')
def PedidoxArticuloForm(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   pedido = Pedidos.objects.filter(id = pk)
   articulo = Pedidos_Articulos.objects.filter(idPedido=pk)
   precio = Articulos.objects.all()
   return render(request, 'Pedidos/ped-art.html', {'pedido': pedido, 'articulo': articulo, 'precio': precio, 'formato': formato})

@permission_required('is_staff')
def PedidoxPiscinaForm(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   pedido = Pedidos.objects.filter(id = pk)
   piscina = Pedidos_Piscinas.objects.filter(idPedido=pk)
   pisc = Piscinas.objects.all()
   return render(request, 'Pedidos/ped-pisc.html', {'pedido': pedido, 'piscina': piscina, 'pisc': pisc, 'formato': formato})

@login_required
def Pedidos_PR(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   pedido = Pedidos.objects.filter(estado='PR')
   return render(request, 'Pedidos/pedido_pr.html', {'pedido': pedido, 'formato': formato})

@login_required
def Pedidos_AR(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   pedido = Pedidos.objects.filter(estado='AR')
   return render(request, 'Pedidos/pedido_ar.html', {'pedido': pedido, 'formato': formato})

@login_required
def Pedidos_EN(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   pedido = Pedidos.objects.filter(estado='EN')
   return render(request, 'Pedidos/pedido_en.html', {'pedido': pedido, 'formato': formato})

@login_required
def Pedidos_DE(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   pedido = Pedidos.objects.filter(estado='DE')
   return render(request, 'Pedidos/pedido_de.html', {'pedido': pedido, 'formato': formato})

@login_required
def Pedidos_CA(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   pedido = Pedidos.objects.filter(estado='CA')
   return render(request, 'Pedidos/pedido_ca.html', {'pedido': pedido, 'formato': formato})

class PedidoCreateView(CreateView):
   model = Pedidos
   form_class = PedidosForm
   template_name = 'Pedidos/pedido_form_create.html'
   success_url= '/pedidos'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      if self.request.POST:
         context['form'] = PedidosForm(self.request.POST)
         context['formset'] = Ped_ArtFormSet(self.request.POST)
         context['formset2'] = Ped_PiscFormSet(self.request.POST)
      else:
         context['form'] = PedidosForm()
         context['formset'] = Ped_ArtFormSet()
         context['formset2'] = Ped_PiscFormSet()
      return context

   def form_valid(self, form):
      context = self.get_context_data()
      form = context['form']
      formset = context['formset']
      formset2 = context['formset2']
      if form.is_valid() and formset.is_valid() and formset2.is_valid():
         self.object = form.save()
         form.instance = self.object
         form.save()
         formset.instance = self.object
         formset.save()
         formset2.instance = self.object
         formset2.save()
         return super().form_valid(form)
      else:
         return self.render_to_response(self.get_context_data(form=form))

class UpdatePedidoView(NamedFormsetsMixin, UpdateWithInlinesView):
   model = Pedidos
   form_class = PedidosForm
   inlines = [Pedido_ArticulosInline, Pedido_PiscinasInline]
   inlines_names = ['Articulos', 'Piscinas']
   template_name = 'Pedidos/pedido_form_update.html'
   success_url= '/pedidos'

class Pedido_ArtCreateView(CreateView):
   form_class = PedidosForm
   template_name = 'Pedidos/pedidoart_form_create.html'

   def get_context_data(self, **kwargs):
      context = super(Pedido_ArtCreateView, self).get_context_data(**kwargs)
      context['Ped_art_formset'] = Ped_ArtFormSet()
      return context

   def post(self, request, *args, **kwargs):
      self.object = None
      form_class = self.get_form_class()
      form = self.get_form(form_class)
      Ped_art_formset = Ped_ArtFormSet(self.request.POST)
      if form.is_valid() and Ped_art_formset.is_valid():
         return self.form_valid(form, Ped_art_formset)
      else:
         return self.form_invalid(form, Ped_art_formset)

   def form_valid(self, form, Ped_art_formset):
      self.object = form.save(commit=False)
      self.object.save()
      # saving ProductMeta Instances
      product_metas = Ped_art_formset.save(commit=False)
      for form2 in product_metas:
         form2.idPedido = self.object
         form2.save()
         Art = Articulos.objects.get(id=form2.idArticulo_id)
         Art.stock -= form2.unidades
         Art.save()
      return redirect("/pedidos")

   def form_invalid(self, form, Ped_art_formset):
      return self.render_to_response(
         self.get_context_data(form=form,
                                 Ped_art_formset=Ped_art_formset
                                 )
      )

class Pedido_PiscCreateView(CreateView):
   form_class = PedidosForm
   template_name = 'Pedidos/pedidopisc_form_create.html'

   def get_context_data(self, **kwargs):
      context = super(Pedido_PiscCreateView, self).get_context_data(**kwargs)
      context['Ped_Pisc_formset'] = Ped_PiscFormSet()
      return context

   def post(self, request, *args, **kwargs):
      self.object = None
      form_class = self.get_form_class()
      form = self.get_form(form_class)
      Ped_Pisc_formset = Ped_PiscFormSet(self.request.POST)
      if form.is_valid() and Ped_Pisc_formset.is_valid():
         return self.form_valid(form, Ped_Pisc_formset)
      else:
         return self.form_invalid(form, Ped_Pisc_formset)

   def form_valid(self, form, Ped_Pisc_formset):
      self.object = form.save(commit=False)
      self.object.save()
      # saving ProductMeta Instances
      product_metas = Ped_Pisc_formset.save(commit=False)
      for form2 in product_metas:
         form2.idPedido = self.object
         form2.save()
         Pisc = Piscinas.objects.get(id=form2.idPiscina_id)
         Pisc.unidades -= form2.unidades
         Pisc.save()

      return redirect("/pedidos")

   def form_invalid(self, form, Ped_Pisc_formset):
      return self.render_to_response(
         self.get_context_data(form=form,
                                 Ped_Pisc_formset=Ped_Pisc_formset
                                 )
      )

# Section - Caja
@login_required
@permission_required('is_staff')
def vCaja(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   caja = Caja.objects.all()
   ingresos = Ingresos.objects.all()
   egresos = Egresos.objects.all()
   context = {'caja': caja, 'ingresos': ingresos, 'egresos': egresos, 'formato': formato}
   
   return render(request, 'Caja/caja.html', context)

@login_required
@permission_required('is_staff')
def vIngreso(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   caja = Caja.objects.all()
   ingresos = Ingresos.objects.all()
   context = {'caja': caja, 'ingresos': ingresos, 'formato': formato}
   return render(request, 'Caja/Ingresos/ingresos.html', context)

@login_required
@permission_required('is_staff')
def vEgreso(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   caja = Caja.objects.all()
   egresos = Egresos.objects.all()
   context = {'caja': caja, 'egresos': egresos, 'formato': formato}
   return render(request, 'Caja/Egresos/egresos.html', context)

class ModCajaView(PermissionRequiredMixin, UpdateView):
   permission_required = 'Application.change_caja'
   model = Caja
   form_class = CajaForm
   template_name = 'Caja/caja-form.html'
   success_url = "/caja"

class ModIngresoView(PermissionRequiredMixin, UpdateView):
   permission_required = 'Application.change_ingresos'
   model = Ingresos
   form_class = IngresosForm
   template_name = 'Caja/Ingresos/ingresos-form.html'
   success_url = "/caja"

class ModEgresoView(PermissionRequiredMixin, UpdateView):
   permission_required = 'Application.change_egresos'
   model = Egresos
   form_class = EgresosForm
   template_name = 'Caja/Egresos/egresos-form.html'
   success_url = "/caja"

class DeleteCajaView(PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_caja'
   model = Caja
   template_name = 'Caja/caja-delete-form.html'
   success_url = "/caja"

class DeleteIngresoView(PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_ingresos'
   model = Ingresos
   template_name = 'Caja/Ingresos/ingresos-delete-form.html'
   success_url = "/caja"

class DeleteEgresoView(PermissionRequiredMixin, DeleteView):
   permission_required = 'Application.delete_egresos'
   model = Egresos
   template_name = 'Caja/Egresos/egresos-delete-form.html'
   success_url = "/caja"

@login_required
@permission_required('is_staff')
def Historico_Caja(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   caja = Caja.objects.all()
   ingresos = Ingresos.objects.all()
   egresos = Egresos.objects.all()
   context = {'caja': caja, 'ingresos': ingresos, 'egresos': egresos, 'formato': formato}
   
   return render(request, 'Caja/historico-caja.html', context)

@permission_required('is_staff')
def CajaxIngreso(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   caja = Pedidos.objects.filter(id=pk)
   ingreso = Ingresos.objects.filter(idCaja=pk)
   return render(request, 'Caja/Ingresos/detail-ingreso.html', {'caja': caja, 'ingreso': ingreso, 'formato': formato})

@permission_required('is_staff')
def CajaxEgreso(request, pk):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   caja = Pedidos.objects.filter(id=pk)
   egreso = Egresos.objects.filter(idCaja=pk)
   return render(request, 'Caja/Egresos/detail-egreso.html', {'caja': caja, 'egreso': egreso, 'formato': formato})

@login_required
def Ingreso_TR(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   fecha = horario.strftime("%d/%m/%Y")
   ingreso = Ingresos.objects.filter(condicion='TR')
   return render(request, 'Caja/Ingresos/ingreso_tr.html', {'ingreso': ingreso, 'formato': formato, 'fecha': fecha})

@login_required
def Ingreso_IM(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   ingreso = Ingresos.objects.filter(condicion='IM')
   return render(request, 'Caja/Ingresos/ingreso_im.html', {'ingreso': ingreso, 'formato': formato})

@login_required
def Ingreso_PA(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   ingreso = Ingresos.objects.filter(condicion='PA')
   return render(request, 'Caja/Ingresos/ingreso_pa.html', {'ingreso': ingreso, 'formato': formato})

@login_required
def Egreso_TR(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   egreso = Egresos.objects.filter(condicion='TR')
   return render(request, 'Caja/Egresos/egreso_tr.html', {'egreso': egreso, 'formato': formato})

@login_required
def Egreso_IM(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   egreso = Egresos.objects.filter(condicion='IM')
   return render(request, 'Caja/Egresos/egreso_im.html', {'egreso': egreso, 'formato': formato})

@login_required
def Egreso_PA(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   egreso = Egresos.objects.filter(condicion='PA')
   return render(request, 'Caja/Egresos/egreso_pa.html', {'egreso': egreso, 'formato': formato})

class IngresosCreateView(PermissionRequiredMixin, CreateView):
   permission_required = 'Application.add_ingresos'

   form_class = CajaForm
   template_name = 'Caja/Ingresos/ingresos_form2.html'

   def get_context_data(self, **kwargs):
      context = super(IngresosCreateView, self).get_context_data(**kwargs)
      context['Ingresos_formset'] = IngresosFormSet()
      return context

   def post(self, request, *args, **kwargs):
      self.object = None
      form_class = self.get_form_class()
      form = self.get_form(form_class)
      Ingresos_formset = IngresosFormSet(self.request.POST)
      if form.is_valid() and Ingresos_formset.is_valid():
         return self.form_valid(form, Ingresos_formset)
      else:
         return self.form_invalid(form, Ingresos_formset)

   def form_valid(self, form, Ingresos_formset):
      self.object = form.save(commit=False)
      self.object.save()
      # saving ProductMeta Instances
      product_metas = Ingresos_formset.save(commit=False)
      for form2 in product_metas:
         form2.idCaja = self.object
         form2.save()
      return redirect('/caja')

   def form_invalid(self, form, Ingresos_formset):
      return self.render_to_response(
         self.get_context_data(form=form,
                                 Ingresos_formset=Ingresos_formset
                                 )
      )

class UpdateIngresoView(NamedFormsetsMixin, UpdateWithInlinesView):
   model = Caja
   form_class = CajaForm
   inlines = [IngresoInline]
   inlines_names = ['Ingresos']
   template_name = 'Caja/Ingresos/ingresos_update.html'
   success_url= '/caja'

class EgresosCreateView(PermissionRequiredMixin, CreateView):
   permission_required = 'Application.add_egresos'

   form_class = CajaForm
   template_name = 'Caja/Egresos/egresos_form2.html'

   def get_context_data(self, **kwargs):
      context = super(EgresosCreateView, self).get_context_data(**kwargs)
      context['Egresos_formset'] = EgresosFormSet()
      return context

   def post(self, request, *args, **kwargs):
      self.object = None
      form_class = self.get_form_class()
      form = self.get_form(form_class)
      Egresos_formset = EgresosFormSet(self.request.POST)
      if form.is_valid() and Egresos_formset.is_valid():
         return self.form_valid(form,Egresos_formset)
      else:
         return self.form_invalid(form, Egresos_formset)

   def form_valid(self, form, Egresos_formset):
      self.object = form.save(commit=False)
      self.object.save()
      # saving ProductMeta Instances
      product_metas = Egresos_formset.save(commit=False)
      for form2 in product_metas:
         form2.idCaja = self.object
         form2.save()
      return redirect('/caja')

   def form_invalid(self, form, Egresos_formset):
      return self.render_to_response(
         self.get_context_data(form=form,
                                 Egresos_formset=Egresos_formset
                                 )
      )

class UpdateEgresoView(NamedFormsetsMixin, UpdateWithInlinesView):
   model = Caja
   form_class = CajaForm
   inlines = [EgresoInline]
   inlines_names = ['Egresos']
   template_name = 'Caja/Egresos/egresos_update.html'
   success_url= '/caja'

@login_required
@permission_required('is_staff')
def grafico_one(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   data = Piscinas.objects.all()
   context = {
      'data': data,
      'formato': formato,
   }
   return render(request, 'Graficos/graficos_1.html', context)

@login_required
@permission_required('is_staff')
def grafico_two(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   data = Piscinas.objects.all()
   context = {
      'data': data,
      'formato': formato,
   }
   return render(request, 'Graficos/graficos_2.html', context)

@login_required
@permission_required('is_staff')
def grafico_three(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   data = Articulos.objects.all()
   context = {
      'data': data,
      'formato': formato,
   }
   return render(request, 'Graficos/graficos_3.html', context)

@login_required
@permission_required('is_staff')
def grafico_four(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   data_clientes = Clientes.objects.count()
   data_proveedores = Proveedores.objects.count()
   data_empleados = Empleados.objects.count()
   context = {
      'data_clientes': data_clientes,
      'data_proveedores': data_proveedores,
      'data_empleados': data_empleados,
      'formato': formato,
   }
   return render(request, 'Graficos/graficos_4.html', context)

@login_required
@permission_required('is_staff')
def grafico_five(request):
   horario = datetime.now()
   formato = horario.strftime("Fecha: %d/%m/%Y - %H:%M hs.")
   data_ad = Empleados.objects.filter(rol__contains = 'AD').count()
   data_ob = Empleados.objects.filter(rol__contains = 'OB').count()
   data_te = Empleados.objects.filter(rol__contains = 'TE').count()
   data_ge = Empleados.objects.filter(rol__contains = 'GE').count()
   data_ve = Empleados.objects.filter(rol__contains = 'VE').count()
   data_lo = Empleados.objects.filter(rol__contains = 'LO').count()
   context = {
      'data_ad': data_ad,
      'data_ob': data_ob,
      'data_te': data_te,
      'data_ge': data_ge,
      'data_ve': data_ve,
      'data_lo': data_lo,
      'formato': formato,
   }
   return render(request, 'Graficos/graficos_5.html', context)

# Section - PDF
class IngresosPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/IngresosPDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'ingreso': Ingresos.objects.all(), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class IngresosPAPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/IngresosPDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'ingreso': Ingresos.objects.filter(condicion='PA'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class IngresosIMPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/IngresosPDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'ingreso': Ingresos.objects.filter(condicion='IM'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class IngresosTRPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/IngresosPDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'ingreso': Ingresos.objects.filter(condicion='TR'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class EgresosPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/EgresosPDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'egreso': Egresos.objects.all(), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class EgresosPAPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/EgresosPDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'egreso': Egresos.objects.filter(condicion='PA'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class EgresosIMPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/EgresosPDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'egreso': Egresos.objects.filter(condicion='IM'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class EgresosTRPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/EgresosPDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'egreso': Egresos.objects.filter(condicion='TR'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class AdquisicionPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/AdquisicionPDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'adquisicion': Adquisicion.objects.all(), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')
      #response['Content-Disposition'] = 'attachment; filename="Adquisicion.pdf"'

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response
   
class Adquisicion_PiscinaPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/Adquisicion_PiscinaPDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'adquisicion': AdquisicionProveedor_Piscinas.objects.all(), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class Adquisicion_ArticuloPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/Adquisicion_ArticuloPDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'adquisicion': AdquisicionProveedor_Articulos.objects.all(), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class AdquisicionxPagoPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/AdquisicionPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'adquisicion': Adquisicion.objects.filter(metodoPago_id=self.kwargs['pk']), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class Adquisicion_ARPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/AdquisicionPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")

      context = {'adquisicion': Adquisicion.objects.filter(estado='AR'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class Adquisicion_CAPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/AdquisicionPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")

      context = {'adquisicion': Adquisicion.objects.filter(estado='CA'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response
   
class Adquisicion_DEPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/AdquisicionPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")

      context = {'adquisicion': Adquisicion.objects.filter(estado='DE'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response
   
class Adquisicion_ENPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/AdquisicionPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")

      context = {'adquisicion': Adquisicion.objects.filter(estado='EN'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class Adquisicion_PRPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/AdquisicionPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")

      context = {'adquisicion': Adquisicion.objects.filter(estado='PR'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class ClientePDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/ClientePDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'cliente': Clientes.objects.all(), 'direccion': Direccion_Cliente.objects.all(), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class ProveedorPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/ProveedorPDF.html')
      context = {'proveedor': Proveedores.objects.all(), 'direccion': Direccion_Proveedor.objects.all()}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class EmpleadoPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/EmpleadoPDF.html')
      context = {'empleado': Empleados.objects.all(), 'direccion': Direccion_Empleado.objects.all()}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class Empleado_AdministrativoPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/EmpleadoPDF.html')
      context = {'empleado': Empleados.objects.filter(rol='AD'), 'direccion': Direccion_Empleado.objects.all()}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class Empleado_ObreroPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/EmpleadoPDF.html')
      context = {'empleado': Empleados.objects.filter(rol='OB'), 'direccion': Direccion_Empleado.objects.all()}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response
   
class Empleado_TemporarioPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/EmpleadoPDF.html')
      context = {'empleado': Empleados.objects.filter(rol='TE'), 'direccion': Direccion_Empleado.objects.all()}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class Empleado_GerenciaPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/EmpleadoPDF.html')
      context = {'empleado': Empleados.objects.filter(rol='GE'), 'direccion': Direccion_Empleado.objects.all()}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class Empleado_VentasPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/EmpleadoPDF.html')
      context = {'empleado': Empleados.objects.filter(rol='VE'), 'direccion': Direccion_Empleado.objects.all()}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response
   
class Empleado_LogisticaPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/EmpleadoPDF.html')
      context = {'empleado': Empleados.objects.filter(rol='LO'), 'direccion': Direccion_Empleado.objects.all()}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class ObraPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/ObraPDF.html')
      context = {'obra': Obras.objects.all(), 'direccion': Direccion_Obras.objects.all()}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class ArticulosPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/ArticulosPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'articulo': Articulos.objects.all(), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response
   
class ArticulosxCategoriaPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/ArticulosxCategoriaPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      context = {'categoria': Categorias.objects.filter(id=self.kwargs['pk']), 'articulo': Articulos.objects.all(), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class AdquisicionesxArticulosPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/AdquisicionesxArticulosPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      context = {'articulo': Articulos.objects.filter(id=self.kwargs['pk']), 'adquisicion': AdquisicionProveedor_Articulos.objects.filter(idArticulo_id=self.kwargs['pk']), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response
   
class PedidosxArticulosPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/PedidosxArticulosPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      context = {'articulo': Articulos.objects.filter(id=self.kwargs['pk']), 'pedido': Pedidos_Articulos.objects.filter(idArticulo_id=self.kwargs['pk']), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class AdquisicionesxPiscinasPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/AdquisicionesxPiscinasPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      context = {'piscina': Piscinas.objects.filter(id=self.kwargs['pk']), 'adquisicion': AdquisicionProveedor_Piscinas.objects.filter(idPiscina_id=self.kwargs['pk']), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response
   
class PedidosxPiscinasPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/PedidosxPiscinasPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      context = {'piscina': Piscinas.objects.filter(id=self.kwargs['pk']), 'pedido': Pedidos_Piscinas.objects.filter(idPiscina_id=self.kwargs['pk']), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class PedidosxClientePDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/PedidosxClientePDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      context = {'cliente': Clientes.objects.filter(dni=self.kwargs['pk']), 'pedido': Pedidos.objects.all(), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class AdquisicionesxProveedorPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/AdquisicionesxProveedorPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      context = {'proveedor': Proveedores.objects.filter(cuit=self.kwargs['pk']), 'adquisicion': Adquisicion.objects.all(), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class CajaxEmpleadoPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/CajaxEmpleadoPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      context = {'empleado': Empleados.objects.filter(dni=self.kwargs['pk']), 'caja': Caja.objects.all(), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class PiscinasPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/PiscinasPDF.html')
      context = {'piscina': Piscinas.objects.all()}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class PedidosPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/PedidosPDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'pedido': Pedidos.objects.all(), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class Pedido_PiscinaPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/Pedido_PiscinaPDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'pedido': Pedidos_Piscinas.objects.all(), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class Pedido_ArticuloPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/Pedido_ArticuloPDF.html')
      
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'pedido': Pedidos_Articulos.objects.all(), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class PedidoxPagoPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/PedidosPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")
      
      context = {'pedido': Pedidos.objects.filter(metodoPago_id=self.kwargs['pk']), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class Pedido_ARPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/PedidosPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")

      context = {'pedido': Pedidos.objects.filter(estado='AR'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class Pedido_CAPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/PedidosPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")

      context = {'pedido': Pedidos.objects.filter(estado='CA'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response
   
class Pedido_DEPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/PedidosPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")

      context = {'pedido': Pedidos.objects.filter(estado='DE'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response
   
class Pedido_ENPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/PedidosPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")

      context = {'pedido': Pedidos.objects.filter(estado='EN'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response

class Pedido_PRPDF(View):

   def get(self, request, *args, **kwargs):

      template = get_template('PDF/PedidosPDF.html')
      horario = datetime.now()
      formato = horario.strftime("%d/%m/%Y - %H:%M hs.")

      context = {'pedido': Pedidos.objects.filter(estado='PR'), 'horario': formato}
      html = template.render(context)
      response = HttpResponse(content_type='application/pdf')

      pisa_status = pisa.CreatePDF(
         html, dest=response)
      return response


def password_reset_request(request):
   if request.method == "POST":
      password_form = PasswordResetForm(request.POST)
      if password_form.is_valid():
         data = password_form.cleaned_data['email']
         user_email = User.objects.filter(Q(email=data))
         if user_email.exists():
               for user in user_email:
                  subject = "Solicitud para Recuperar contraseña"
                  email_template_name = "Password/password_reset_email.html"
                  context = {
                     'user': user.username,
                     'email': user.email,
                     'domain': '127.0.0.1:8000',
                     'site_name': 'EMB Piscinas',
                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                     'token': default_token_generator.make_token(user),
                     'protocol': 'http',
                  }
                  email_html = render_to_string(email_template_name, context)
                  email_plain = "Password/password_reset_email.txt"
                  email = EmailMultiAlternatives(
                     subject=subject,
                     body=email_plain,
                     from_email='',
                     to=[user.email]
                  )
                  email.attach_alternative(email_html, "text/html")
                  email.send()
               return redirect('password_reset_done')
   else:
      password_form = PasswordResetForm()
   context = {
      'password_form': password_form,
   }
   return render(request, 'Password/password_reset.html', context)