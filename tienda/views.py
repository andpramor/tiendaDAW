from decimal import Decimal
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Sum, Count
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from .models import *
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

def welcome(request):
    return render(request,'tienda/index.html', {})

class Listado(ListView):
    model = Producto
    template_name = 'tienda/listado.html'
    ordering = ['nombre']

class CreateProducto(CreateView): #CREATE
    model = Producto
    fields = ['marca','nombre','modelo','unidades','precio','vip']
    template_name = 'tienda/createProducto.html'
    success_url = reverse_lazy('listado')

class DetailProducto(DetailView): #READ
    model = Producto
    template_name = 'tienda/readProducto.html'

class UpdateProducto(UpdateView): #UPDATE
    model = Producto
    fields = ['marca','nombre','modelo','unidades','precio','vip']
    template_name = 'tienda/updateProducto.html'
    success_url = reverse_lazy('listado')

class DeleteProducto(DeleteView): #DELETE
    model = Producto
    template_name = 'tienda/deleteProducto.html'
    success_url = reverse_lazy('listado')

class Tienda(ListView):
    model = Producto
    template_name = 'tienda/tienda.html'
    ordering = ['nombre']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        productos = Producto.objects.all()
        modelos = sorted(set(producto.modelo for producto in productos))
        marcas = sorted(set(Marca.objects.values_list('nombre',flat=True)))
        #flat=True se usa para tener sólo los valores en una lista, en lugar de una lista de tuplas.
        marca = self.request.GET.get('marca')
        modelo = self.request.GET.get('modelo')
        busqueda = self.request.GET.get('busqueda')
        productosFiltrados = self.get_queryset()
        context['productos'] = productosFiltrados
        context['marcas'] = marcas
        context['modelos'] = modelos
        context['marca_seleccionada'] = marca
        context['modelo_seleccionado'] = modelo
        context['busqueda'] = busqueda
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        marca = self.request.GET.get('marca')
        modelo = self.request.GET.get('modelo')
        busqueda = self.request.GET.get('busqueda')
        if marca:
            queryset = queryset.filter(marca__nombre__iexact=marca)
        if modelo:
            queryset = queryset.filter(modelo=modelo)
        if busqueda:
            queryset = queryset.filter(nombre__icontains=busqueda)
        return queryset

class Comprar(View):
    def get(self,request,pk):
        producto = Producto.objects.get(pk=pk)
        return render(request,'tienda/comprar.html', {'producto':producto})
    def post(self,request,pk):
        producto = Producto.objects.get(pk=pk)
        unidades = int(request.POST.get('unidades'))
        precio = Decimal(producto.precio)
        usuario = self.request.user
        conIva = Decimal(1.21)
        importe = Decimal(precio*unidades*conIva)
        if producto.unidades >= unidades:
            if importe <= usuario.saldo:
                usuario.saldo -= importe
                usuario.save()
                producto.unidades -= unidades
                producto.save()
                compra = Compra.objects.create(
                    producto = producto,
                    usuario = usuario,
                    unidades = unidades,
                    importe = importe
                )
                #compra.save() no hace falta porque estamos usando create, usando compra = Compra() y luego dándole los datos tipo compra.usuario y asignando uno a uno si porque estamos cambiando el registro de esa compra.
                return redirect('gracias', pk=compra.pk)
        return redirect('welcome') #Redirigiría a donde le diga cuál es el error, si saldo o unidades

class Gracias(DetailView):
    model = Compra
    template_name = 'tienda/gracias.html'

class InformeMarcas(ListView):
    model = Producto
    template_name = 'tienda/informeMarcas.html'
    ordering = ['nombre']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        marcas = sorted(set(Marca.objects.values_list('nombre',flat=True)))
        #flat=True se usa para tener sólo los valores en una lista, en lugar de una lista de tuplas.
        marcaSeleccionada = self.request.GET.get('marca')
        productosFiltrados = self.get_queryset()
        context['productos'] = productosFiltrados
        context['marcas'] = marcas
        context['marca_seleccionada'] = marcaSeleccionada
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        marca = self.request.GET.get('marca')
        if marca:
            queryset = queryset.filter(marca__nombre__iexact=marca)
        return queryset

class InformeTopTen(ListView):
    model = Producto
    template_name = 'tienda/informeTopTenProductos.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = Producto.objects.annotate(sum_ventas=Sum('compra__unidades'),sum_importe=Sum('compra__importe')).order_by('-sum_ventas')[:10]
        return queryset

class InformeComprasUsuario(ListView):
    model = Compra
    template_name = 'tienda/informeComprasUsuario.html'
    ordering = ['-fecha']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cliente_seleccionado = self.request.GET.get('cliente')
        clientes = Usuario.objects.all()
        nombresClientes = sorted(set(cliente.username for cliente in clientes))
        context['clientes'] = nombresClientes
        context['cliente_seleccionado'] = cliente_seleccionado
        queryset = self.get_queryset()
        context['compras'] = queryset
        return context

    def get_queryset(self) -> QuerySet[Any]:
        queryset = Compra.objects.all()
        cliente = self.request.GET.get('cliente')
        if cliente:
            queryset = Compra.objects.filter(usuario__username__iexact=cliente)
        return queryset

class InformeTopTenClientes(ListView):
    model = Usuario
    template_name = 'tienda/informeTopTenClientes.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = Usuario.objects.annotate(sum_importe=Sum('compra__importe')).order_by('-sum_importe')[:10]
        return queryset