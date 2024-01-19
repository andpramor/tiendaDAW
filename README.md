[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=13374774&assignment_repo_type=AssignmentRepo)
# DWES -Django-Models

El objetivo de esta práctica es profundizar en los modelos de Django.
Se pretende crear una aplicación que permita gestionar la base de una 
aplicación web de venta de productos.

![Modelos a crear](Modelos.png)

Se solicita:

## Versión 1.0
* **Creación de los modelos** necesarios para su alta y administración 
en django admin
* **CRUD de productos** en la ruta tienda/admin/productos
   * **listado** de los productos de la tienda
      * Debe tener enlaces para el resto de acciones 
   * **edicion/\<int:pk>** Editar información de un producto
   * **eliminar/\<int:pk>** Debe solicitar confirmación
   * **nuevo** Permite introducir un nuevo producto
* **Compra de productos**. Tiene lugar en la URL tienda/
  * **compra** se muestra un listado de los productos y es posible buscar 
  y filtrar por varios campos.
  * **checkout** se muestra información detallada del producto, se introducen 
  las unidades y se confirma la compra.
* **Informes** En la ruta tienda/informes/
  * Productos por marca. Primero muestra las marcas y 
  después un listado con los productos de la marca que se seleccione
  * Top ten productos vendidos. Mayor número de unidades vendidas
  * Compras de un usuario con acceso al detalle de cada compra.
  * Top ten mejores clientes. Por importe gastado.
* **Login** 
  * Incluye en el template base un apartado que identifique si el usuario
  está o no logado, dando opciones de login o logout según proceda
  * Crea un formulario de login que permita autenticar y logar 
  únicamente a los clientes (No se permite login de usuarios que no tengan
  relación con el modelo cliente)
  * El login devuelve a la página desde la que se redirigió.
* **Control de Permisos** 
  * Las secciones de Informes, Admin y CRUD de productos son sólo
  para usuarios tipo superuser y staff
  * La vista de checkout debe estar restringida a usuarios registrados
  cómo clientes.
  * Las vistas de productos de la tienda y detalle de producto son de
  acceso público.
  
## Versión 2.0 
* **Creación de los modelos** para la gestión de promociones
* **CRUD de promociones** en la ruta tienda/admin/promociones/
   * **listado** de los productos de la tienda
      * Debe tener enlaces para el resto de acciones 
   * **edicion/\<int:pk>** Editar información de un producto
   * **eliminar/\<int:pk>** Debe solicitar confirmación
   * **nuevo** Permite introducir un nuevo producto
* **Compra de productos**. Ampliación de funcionalidades
  * **checkout** Permite introducir un código de promoción, valida si la promoción es aplicable y muestra el descuento
  antes de confirmar la compra.
* **Informes** En la ruta tienda/informes/
  * **Datos de promociones**. Muestra un informe con el número de compras realizadas
    con cada promoción. Al final muestra un resumen con la cifra total de compras promocionadas
    e información del descuento medio aplicado a las cuentas con promoción.
