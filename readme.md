# DUCKEMB para EMB Piscinas

![Badge de estado](https://img.shields.io/badge/Estado-En%20Desarrollo-brightgreen)
![Badge de versionamiento](https://img.shields.io/badge/Version-0.9-blue)
![Badge de tamaño](https://img.shields.io/badge/Tama%C3%B1o-536%20KB-blue)
![Badge de plataforma](https://img.shields.io/badge/Plataforma-Windows-lightgrey)
![Badge de licencia](https://img.shields.io/badge/Licencia-GPL-green)

El repositorio es parte de un proyecto de desarrollo para las catedras de **Interfaz de Usuario**, **Programación III** y **Práctica Profesionalizante II** de la carrera de **Tecnicatura Superior en Desarrollo de Software** del **Instituto Superior Dr. Carlos Maria Carena** de la localidad de Mina Clavero, en la provincia de Córdoba, Argentina. Este proyecto sirve como parte de una producción de un sistema informatizado para el negocio EMB Piscinas, ubicado en la localidad de Nono, provincia de Córdoba.

Este mismo busca servir como constancia de aprendizaje y desarrollo durante la carrera, y tambien como emprendimiento para dar visibilidad a los conocimientos de los integrantes. Es asi que bajo el nombre del producto **DuckEMB** se intenta dar herramientas a dicho establecimiento en base a sus requerimientos.

Cabe aclarar que se encuentra en las ultimas fases del desarrollo, por lo que es una versión beta del sistema, y es por cuestiones educativos un comprobante para la presentación correspondiente al tribunal de examen impartido por los profesores **Luis Tettamanti**, **Carlos Murua**, **Cristian Cornejo** del día 29 de Marzo de 2023.

(**Aclaración:** Lo que se visualiza en este repositorio es unicamente la parte realizada por mi persona, lo correspondiente a mi compañero sera mostrado cuando el disponga en su respectivo repositorio si asi lo desea).

## Descripción del proyecto 📋

Este proyecto permite funciona como un sistema de gestion de el usuarios (Empleados, Clientes y Proveedores), inventario, informes y registros contables.

Funciona de manera similar a un sistema de Punto de Venta, donde en este caso el mismo genera **Pedidos** y **Adquisiciones** para el manejo comercial del negocio y cuenta con complementos de gestion de personal, contables y de inventario para facilitar al usuario de dicho sistema.

Para mayor información dirigirse a este link. **[Documentación del Proyecto](https://drive.google.com/drive/folders/1bTbYp9bOULH4-wuvgaC4aCwyT77G1lg8?usp=sharing)**

## Tecnologías y plugins utilizados 🛠️

* **`Python`**: Es el lenguaje de programación que utilizaremos para la codificación de funciones y objetos que seran llamados para la creación y estructuración desde la parte del servidor WEB.
* **`Django`**: Es un framework web de alto nivel de Python que se encarga del rápido desarrollo y el diseño limpio y pragmático de páginas WEB.
* **`HTML`**: Para el estructurado de los contenidos de la página WEB.
* **`CSS`**: Para el manejo de estilos de los contenidos de la página WEB
* **`Bootstrap 5`**: Para el manejo de estilos y comportamientos de los contenidos de la página WEB
* **`Javascript`**: Para uso de scripts y el manejo de comportamientos dentro de los contenidos de la página WEB.
* **`JQuery`**: Para uso de plugins y herramientas de los contenidos de la página WEB.
* **`Datatables`**: Para la elaboración de tablas de contenidos dinamicas e interactuables.
* **`Select2`**: Para funcionalidades de los componentes select del proyecto.
* **`HTML2PDF`**: Para la impresión de contenido en formato PDF.
* **`SQLite3`**: Como base de datos relacional por defecto que viene vinculada a los proyectos de Django.
* **`Nativefier`**: Herramienta para la creación de la aplicación de escritorio del proyecto. Se necesita contar con **`NodeJS`** y hace uso de **`Electron`**.

## Instalación 🔧

Para hacer uso de este repositorio es recomendable seguir los siguientes pasos, y en caso de que ya se cuente con el mismo instalado se puede saltear.

* **Paso 1**: Instalación de Python. Para esto puede dirigirse a este link. **[Python]https://www.python.org/downloads/**

* **Paso 2**: Una vez instalado, ingresar a la carpeta del repositorio y abrir el CMD. Una vez abierta la consola escribiremos a continuación lo siguiente, esto nos servira para tener un entorno de trabajo que contenga los requerimientos del sistema:

```
python -m venv <Nombre del Entorno Virtual>
```

* **Paso 3**: Posicionarse en el nuevo directorio y entrar a la carpeta de scripts, para asi activar el entorno.

```
cd <Nombre del Entorno Virtual>
cd scripts
activate
```

* **Paso 4**: Volver hacia la carpeta principal del repositorio, e ingresar a la misma para descargar todos los requerimientos del proyecto.

```
cd ..
cd ..
pip install -r requirements.txt
```

* **Paso 5**: Ya instalada todas las dependencias. Ingresar la siguiente linea de comando nos ubicaremos en la carpeta del proyecto para inicializar el servidor local:

```
cd DuckEMB_Project
python manage.py runserver
```

* **Paso 6**: Ingresar al navegador WEB y escribir la siguiente dirección para entrar a la página WEB:

```
127.0.0.1:8000/login
```

Ya a partir de este punto puede utilizar sin problemas el repositorio.

Para acceder a las funcionalidades de cada rol del sistema puede utilizar los siguientes usuarios de ejemplo con contraseña:

**Usuario:**
    Nombre de Usuario: user
    Contraseña: pato3476

**Empleado:**
    Nombre de Usuario: staff
    Contraseña: duck1298

**Administrador:**
    Nombre de Usuario: admin
    Contraseña: admin123

## Autor ✒️

Este repositorio ha sido construido por:

* **[Matías J. Meda](https://github.com/MED4CHON)**

## Licencia 📄

Este proyecto está bajo la Licencia (GPL). Esta es una licencia de software libre copyleft donde cualquiera de los usuarios de un programa con licencia GPL pueden libres de usar y acceder al código fuente de este repositorio, y realizar modificaciones y poder distribuir los cambios siempre que redistribuya el programa completo (modificado o no modificado) bajo esta misma licencia.
