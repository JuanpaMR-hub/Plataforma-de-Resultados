from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Ulearnet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_ulearnet = models.IntegerField()



class Letra(models.Model):
    idletra = models.IntegerField(primary_key=True)
    letra_id = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'letra'


class Nivel(models.Model):
    idnivel = models.IntegerField(primary_key=True)
    nombre_nivel = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'nivel'


class PagesActividad(models.Model):
    id_actividad = models.IntegerField(primary_key=True)
    nombre_actividad = models.CharField(max_length=100)
    grafico = models.CharField(max_length=800)

    class Meta:
        managed = False
        db_table = 'pages_actividad'


class Pertenece(models.Model):
    fecha = models.CharField(primary_key=True, max_length=45)
    usuario_id = models.CharField(max_length=45)
    colegio_id = models.CharField(max_length=45)
    nivel_id = models.CharField(max_length=45)
    letra_id = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'pertenece'
        unique_together = (('fecha', 'usuario_id', 'colegio_id', 'nivel_id', 'letra_id'),)


class Usuario(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    usuario = models.CharField(max_length=45, blank=True, null=True)
    contrasena = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'


class Colegio(models.Model):
    idcolegio = models.IntegerField(db_column='idColegio', primary_key=True)  # Field name made lowercase.
    nombre_colegio = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'colegio'


class Actividadxreim(models.Model):
    id_actividad = models.IntegerField()
    id_reim = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'actividadxreim'
        unique_together = (('id_reim', 'id_actividad'),)
