from django.db import models

# Create your models here.


class Actividad(models.Model):
    id_actividad = models.IntegerField(primary_key=True)
    nombre_actividad = models.CharField(max_length=100)
    grafico = models.CharField(max_length=800)

