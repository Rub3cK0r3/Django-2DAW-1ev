from django.db import models
from django.urls import reverse
# Create your models here.

# Modelo de la nueva implementacion para la gestion de editores
class Editor(models.Model):
    # el id me lo gestiona el internamente haciendolo incremental, `la primarykey será el id que genera`

    nif = models.CharField(max_length=12,unique=True) # pero no es la primary key
    
    email = models.EmailField()
    telefono = models.CharField(max_length=9) # simulando que es un telefono real
    pais = models.CharField(max_length=100) # una cadena que contiene el pais no es ninguna relacion

    # como es una cadena relativamente  corta uso el max_lenght
    nombre = models.CharField(max_length=100)
    nombre_comercial = models.CharField(max_length=100)

    # muy util para gestionar las url de las detailview mas adelante
    def get_absolute_url(self):
        return reverse('appprueba:editor_detail', args=[str(self.id)])

    def __str__(self):
        return self.nombre # elijo que cuando visione un objeto de este tipo me muestre su nombreclass Editor(models.Model):
    nif