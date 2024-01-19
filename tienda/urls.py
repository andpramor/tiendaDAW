from django.urls import path
from . import views
from tienda.views import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/admin/productos/listado', staff_member_required(Listado.as_view()), name='listado'),
    path('tienda/admin/productos/nuevo/', staff_member_required(CreateProducto.as_view()), name='createProducto'),
    path('tienda/admin/productos/detalleProducto/<int:pk>', staff_member_required(DetailProducto.as_view()), name='detailProducto'),
    path('tienda/admin/productos/edicion/<int:pk>', staff_member_required(UpdateProducto.as_view()), name='updateProducto'),
    path('tienda/admin/productos/eliminar/<int:pk>', staff_member_required(DeleteProducto.as_view()), name='deleteProducto'),
    path('tienda/', Tienda.as_view(), name='tienda'),
    path('tienda/comprar/<int:pk>', login_required(Comprar.as_view()), name='comprar'),
    path('tienda/gracias/<int:pk>', Gracias.as_view(), name='gracias'),
    path('tienda/informes/por_marca', staff_member_required(InformeMarcas.as_view()), name='informeMarcas'),
    path('tienda/informes/top_productos', staff_member_required(InformeTopTen.as_view()), name='informeTopTenProductos'),
    path('tienda/informes/compras_usuario', staff_member_required(InformeComprasUsuario.as_view()), name='informeComprasUsuario'),
    path('tienda/informes/top_clientes', staff_member_required(InformeTopTenClientes.as_view()), name='informeTopTenClientes'),
]