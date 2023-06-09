# Generated by Django 4.1.3 on 2023-04-11 01:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adquisicion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('PR', 'En proceso'), ('AR', 'Armado'), ('EN', 'En entrega'), ('DE', 'Despachado'), ('CA', 'Cancelado')], max_length=15)),
                ('fechaEntrega', models.DateField(help_text='Fecha de Entrega', verbose_name='Entregado')),
                ('fechaRecibido', models.DateField(blank=True, help_text='Fecha de Recibo', null=True, verbose_name='Recibido')),
            ],
        ),
        migrations.CreateModel(
            name='AdquisicionProveedor_Piscinas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidades', models.PositiveIntegerField(help_text='Unidades a ingresar', verbose_name='Unidades')),
                ('idAdquisicion', models.ForeignKey(help_text='Adquisicion', on_delete=django.db.models.deletion.CASCADE, to='Application.adquisicion', verbose_name='Adquisicion')),
            ],
        ),
        migrations.CreateModel(
            name='Articulos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=60, verbose_name='Descripción')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('porcentaje', models.DecimalField(decimal_places=2, help_text='Equivalencia: 1.00 = 100%', max_digits=3)),
                ('stock', models.IntegerField(verbose_name='Stock')),
                ('marca', models.CharField(max_length=30, verbose_name='Marca')),
                ('modelo', models.CharField(blank=True, max_length=60, verbose_name='Modelo')),
                ('imagen', models.ImageField(blank=True, default='emb-logo.png', upload_to='Images/Articulos', verbose_name='Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(help_text='Fecha', verbose_name='Fecha')),
                ('tipo', models.CharField(choices=[('IN', 'Ingresos'), ('EG', 'Egresos')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=30, verbose_name='Categoria')),
                ('imagen', models.ImageField(blank=True, default='emb-logo.png', help_text='Imagen del articulo', upload_to='Images/Categorias', verbose_name='Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('dni', models.CharField(help_text='Numero de Identidad', max_length=9, primary_key=True, serialize=False, verbose_name='DNI')),
                ('nombre', models.CharField(blank=True, help_text='Nombre del Cliente', max_length=50, verbose_name='Nombre')),
                ('telefono', models.CharField(blank=True, help_text='Telefono del Cliente', max_length=14, verbose_name='Telefono')),
                ('email', models.EmailField(blank=True, help_text='e-Mail del Cliente', max_length=254, verbose_name='e-Mail')),
                ('imagen', models.ImageField(blank=True, default='emb-logo.png', help_text='Imagen del articulo', upload_to='Images/Clientes', verbose_name='Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Empleados',
            fields=[
                ('dni', models.CharField(help_text='Numero de Identidad', max_length=9, primary_key=True, serialize=False, verbose_name='DNI')),
                ('nombre', models.CharField(help_text='Nombre del Empleado', max_length=50, verbose_name='Nombre')),
                ('telefono', models.CharField(blank=True, help_text='Telefono del Empleado', max_length=14, verbose_name='Telefono')),
                ('email', models.EmailField(blank=True, help_text='e-Mail del Empleado', max_length=254, verbose_name='e-Mail')),
                ('rol', models.CharField(choices=[('AD', 'Administrativo'), ('OB', 'Obrero'), ('TE', 'Temporario'), ('GE', 'Gerencia'), ('VE', 'Ventas'), ('LO', 'Logistica')], max_length=20, verbose_name='Rol')),
                ('imagen', models.ImageField(blank=True, default='emb-logo.png', help_text='Imagen del articulo', upload_to='Images/Empleados', verbose_name='Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Ingresos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.PositiveIntegerField(help_text='Valor ingresado', verbose_name='Valor')),
                ('condicion', models.CharField(choices=[('TR', 'En tramite'), ('IM', 'Impago'), ('PA', 'Pagado')], default='TR', max_length=20)),
                ('idCaja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Application.caja', verbose_name='Caja')),
            ],
        ),
        migrations.CreateModel(
            name='Metodos_Pagos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metodoPago', models.CharField(max_length=40, verbose_name='Medio de Pago')),
            ],
        ),
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('PR', 'En proceso'), ('AR', 'Armado'), ('EN', 'En entrega'), ('DE', 'Despachado'), ('CA', 'Cancelado')], default='PR', max_length=15)),
                ('fecha', models.DateField(default=datetime.date.today, help_text='Fecha del pedido', verbose_name='Fecha')),
            ],
        ),
        migrations.CreateModel(
            name='Pedidos_Piscinas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidades', models.PositiveIntegerField(help_text='Unidades a ingresar', verbose_name='Unidades')),
                ('idPedido', models.ForeignKey(help_text='Pedido', on_delete=django.db.models.deletion.CASCADE, to='Application.pedidos', verbose_name='Pedido')),
            ],
        ),
        migrations.CreateModel(
            name='Proveedores',
            fields=[
                ('cuit', models.CharField(help_text='Numero de Identidad', max_length=12, primary_key=True, serialize=False, verbose_name='CUIT')),
                ('nombre', models.CharField(blank=True, help_text='Nombre del Proveedor', max_length=50, verbose_name='Nombre')),
                ('telefono', models.CharField(blank=True, help_text='Telefono del Proveedor', max_length=14, verbose_name='Telefono')),
                ('email', models.EmailField(blank=True, help_text='e-Mail del Proveedor', max_length=254, verbose_name='e-Mail')),
                ('imagen', models.ImageField(blank=True, default='emb-logo.png', help_text='Imagen del articulo', upload_to='Images/Proveedores', verbose_name='Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Provincias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provincia', models.CharField(max_length=40, verbose_name='Provincia')),
            ],
        ),
        migrations.CreateModel(
            name='Piscinas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(help_text='Descripción de la piscina', max_length=60, verbose_name='Descripción')),
                ('unidades', models.IntegerField(help_text='Unidades', verbose_name='Unidades')),
                ('base', models.IntegerField(verbose_name='BASE')),
                ('sf_casilla', models.IntegerField(verbose_name='SF Casilla')),
                ('ac', models.IntegerField(verbose_name='AC')),
                ('al', models.IntegerField(verbose_name='AL')),
                ('ah', models.IntegerField(verbose_name='AH')),
                ('mam', models.IntegerField(verbose_name='M-A-M')),
                ('imagen', models.ImageField(blank=True, default='emb-logo.png', help_text='Imagen del articulo', upload_to='Images/Piscinas', verbose_name='Imagen')),
                ('adquisicionPisc', models.ManyToManyField(through='Application.AdquisicionProveedor_Piscinas', to='Application.adquisicion')),
                ('pedidosPisc', models.ManyToManyField(through='Application.Pedidos_Piscinas', to='Application.pedidos')),
            ],
        ),
        migrations.AddField(
            model_name='pedidos_piscinas',
            name='idPiscina',
            field=models.ForeignKey(help_text='Piscinas', on_delete=django.db.models.deletion.CASCADE, to='Application.piscinas', verbose_name='Piscina'),
        ),
        migrations.CreateModel(
            name='Pedidos_Articulos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidades', models.PositiveIntegerField(help_text='Unidades a ingresar', verbose_name='Unidades')),
                ('idArticulo', models.ForeignKey(help_text='Articulos', on_delete=django.db.models.deletion.CASCADE, to='Application.articulos', verbose_name='Articulos')),
                ('idPedido', models.ForeignKey(help_text='Pedido', on_delete=django.db.models.deletion.CASCADE, to='Application.pedidos', verbose_name='Pedido')),
            ],
        ),
        migrations.AddField(
            model_name='pedidos',
            name='articulo',
            field=models.ManyToManyField(through='Application.Pedidos_Articulos', to='Application.articulos'),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='idCliente',
            field=models.ForeignKey(help_text='Identificador del Cliente', on_delete=django.db.models.deletion.CASCADE, to='Application.clientes', verbose_name='Cliente'),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='ingreso',
            field=models.ManyToManyField(through='Application.Ingresos', to='Application.caja'),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='metodoPago',
            field=models.ForeignKey(help_text='Medio de Pago', on_delete=django.db.models.deletion.CASCADE, to='Application.metodos_pagos', verbose_name='Medio de Pago'),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='piscina',
            field=models.ManyToManyField(through='Application.Pedidos_Piscinas', to='Application.piscinas'),
        ),
        migrations.CreateModel(
            name='Obras',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fechaInicio', models.DateField(blank=True, help_text='Fecha de inicio de Obra', verbose_name='Inicio')),
                ('fechaFinal', models.DateField(blank=True, help_text='Fecha de final de Obra', null=True, verbose_name='Final')),
                ('idEmpleado', models.ForeignKey(help_text='Empleado', on_delete=django.db.models.deletion.CASCADE, to='Application.empleados', verbose_name='Solicitado por:')),
                ('numeroPedido', models.ForeignKey(help_text='Numero de Pedido', on_delete=django.db.models.deletion.CASCADE, to='Application.pedidos', verbose_name='Numero de Pedido')),
            ],
        ),
        migrations.AddField(
            model_name='ingresos',
            name='idPedido',
            field=models.ForeignKey(help_text='Pedido', on_delete=django.db.models.deletion.CASCADE, to='Application.pedidos', verbose_name='Pedido'),
        ),
        migrations.AddField(
            model_name='ingresos',
            name='metodoPago',
            field=models.ForeignKey(help_text='Medio de Pago', on_delete=django.db.models.deletion.CASCADE, to='Application.metodos_pagos', verbose_name='Medio de Pago'),
        ),
        migrations.CreateModel(
            name='Egresos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.PositiveIntegerField(help_text='Valor ingresado', verbose_name='Valor')),
                ('condicion', models.CharField(choices=[('TR', 'En tramite'), ('IM', 'Impago'), ('PA', 'Pagado')], default='TR', max_length=20)),
                ('idAdquisicion', models.ForeignKey(help_text='Adquisicion', on_delete=django.db.models.deletion.CASCADE, to='Application.adquisicion', verbose_name='Adquisicion')),
                ('idCaja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Application.caja', verbose_name='Caja')),
                ('metodoPago', models.ForeignKey(help_text='Medio de Pago', on_delete=django.db.models.deletion.CASCADE, to='Application.metodos_pagos', verbose_name='Medio de Pago')),
            ],
        ),
        migrations.CreateModel(
            name='Direccion_Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle', models.CharField(blank=True, help_text='Calle', max_length=100, verbose_name='Calle')),
                ('barrio', models.CharField(blank=True, help_text='Barrio', max_length=40, verbose_name='Barrio')),
                ('ciudad', models.CharField(blank=True, help_text='Ciudad', max_length=40, verbose_name='Ciudad')),
                ('cp', models.IntegerField(blank=True, help_text='Codigo Postal', verbose_name='CP')),
                ('idProveedor', models.ForeignKey(help_text='Proveedor', on_delete=django.db.models.deletion.CASCADE, to='Application.proveedores', verbose_name='Proveedor')),
                ('provincia', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Application.provincias', verbose_name='Provincia')),
            ],
        ),
        migrations.CreateModel(
            name='Direccion_Obras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle', models.CharField(blank=True, help_text='Calle', max_length=100, verbose_name='Calle')),
                ('barrio', models.CharField(blank=True, help_text='Barrio', max_length=40, verbose_name='Barrio')),
                ('ciudad', models.CharField(blank=True, help_text='Ciudad', max_length=40, verbose_name='Ciudad')),
                ('cp', models.IntegerField(blank=True, help_text='Codigo Postal', verbose_name='CP')),
                ('idObra', models.ForeignKey(help_text='Obra', on_delete=django.db.models.deletion.CASCADE, to='Application.obras', verbose_name='Obra')),
                ('provincia', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Application.provincias', verbose_name='Provincia')),
            ],
        ),
        migrations.CreateModel(
            name='Direccion_Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle', models.CharField(blank=True, help_text='Calle', max_length=100, verbose_name='Calle')),
                ('barrio', models.CharField(blank=True, help_text='Barrio', max_length=40, verbose_name='Barrio')),
                ('ciudad', models.CharField(blank=True, help_text='Ciudad', max_length=40, verbose_name='Ciudad')),
                ('cp', models.IntegerField(blank=True, help_text='Codigo Postal', verbose_name='CP')),
                ('idEmpleado', models.ForeignKey(help_text='Empleado', on_delete=django.db.models.deletion.CASCADE, to='Application.empleados', verbose_name='Empleado')),
                ('provincia', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Application.provincias', verbose_name='Provincia')),
            ],
        ),
        migrations.CreateModel(
            name='Direccion_Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle', models.CharField(blank=True, help_text='Calle', max_length=100, verbose_name='Calle')),
                ('barrio', models.CharField(blank=True, help_text='Barrio', max_length=40, verbose_name='Barrio')),
                ('ciudad', models.CharField(blank=True, help_text='Ciudad', max_length=40, verbose_name='Ciudad')),
                ('cp', models.IntegerField(blank=True, help_text='Codigo Postal', verbose_name='CP')),
                ('idCliente', models.ForeignKey(blank=True, help_text='Cliente', null=True, on_delete=django.db.models.deletion.CASCADE, to='Application.clientes', verbose_name='Cliente')),
                ('provincia', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Application.provincias', verbose_name='Provincia')),
            ],
        ),
        migrations.AddField(
            model_name='caja',
            name='egresoCaja',
            field=models.ManyToManyField(through='Application.Egresos', to='Application.adquisicion'),
        ),
        migrations.AddField(
            model_name='caja',
            name='idEmpleado',
            field=models.ForeignKey(help_text='Empleado', on_delete=django.db.models.deletion.CASCADE, to='Application.empleados', verbose_name='Empleado'),
        ),
        migrations.AddField(
            model_name='caja',
            name='ingresoCaja',
            field=models.ManyToManyField(through='Application.Ingresos', to='Application.pedidos'),
        ),
        migrations.AddField(
            model_name='articulos',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Application.categorias', verbose_name='Categoria'),
        ),
        migrations.AddField(
            model_name='articulos',
            name='pedidosArtic',
            field=models.ManyToManyField(through='Application.Pedidos_Articulos', to='Application.pedidos'),
        ),
        migrations.AddField(
            model_name='adquisicionproveedor_piscinas',
            name='idPiscina',
            field=models.ForeignKey(help_text='Piscina', on_delete=django.db.models.deletion.CASCADE, to='Application.piscinas', verbose_name='Piscina'),
        ),
        migrations.CreateModel(
            name='AdquisicionProveedor_Articulos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidades', models.PositiveIntegerField(help_text='Unidades a ingresar', verbose_name='Unidades')),
                ('idAdquisicion', models.ForeignKey(help_text='Adquisicion', on_delete=django.db.models.deletion.CASCADE, to='Application.adquisicion', verbose_name='Adquisicion')),
                ('idArticulo', models.ForeignKey(help_text='Articulos', on_delete=django.db.models.deletion.CASCADE, to='Application.articulos', verbose_name='Articulo')),
            ],
        ),
        migrations.AddField(
            model_name='adquisicion',
            name='articulo',
            field=models.ManyToManyField(through='Application.AdquisicionProveedor_Articulos', to='Application.articulos'),
        ),
        migrations.AddField(
            model_name='adquisicion',
            name='egreso',
            field=models.ManyToManyField(through='Application.Egresos', to='Application.caja'),
        ),
        migrations.AddField(
            model_name='adquisicion',
            name='idProveedor',
            field=models.ForeignKey(help_text='Identificador del Proveedor', on_delete=django.db.models.deletion.CASCADE, to='Application.proveedores', verbose_name='Proveedor'),
        ),
        migrations.AddField(
            model_name='adquisicion',
            name='metodoPago',
            field=models.ForeignKey(help_text='Medio de Pago', on_delete=django.db.models.deletion.CASCADE, to='Application.metodos_pagos', verbose_name='Medio de Pago'),
        ),
        migrations.AddField(
            model_name='adquisicion',
            name='piscina',
            field=models.ManyToManyField(through='Application.AdquisicionProveedor_Piscinas', to='Application.piscinas'),
        ),
    ]
