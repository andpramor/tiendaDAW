from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone

class Usuario(AbstractUser):
    vip = models.BooleanField(default=False)
    saldo = models.DecimalField(default=0.00, decimal_places=2, max_digits=8)

    def __str__(self) -> str:
        return super().__str__()
    
class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.nombre

class Producto(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    unidades = models.PositiveIntegerField() #Stock, meter el validator para minimo 0 y tal.
    precio = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(limit_value=0)])
    vip = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.marca} {self.modelo}'

    class Meta:
        unique_together = ['marca','modelo']

class Compra(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)
    unidades = models.IntegerField()
    iva = models.DecimalField(max_digits= 3, decimal_places=2, default=0.21)
    importe = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ['usuario','fecha','producto']