from django.db import models
from django.contrib.auth.models import User


class Servicio(models.Model):
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=60)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
