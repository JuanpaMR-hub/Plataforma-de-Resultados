from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save, pre_migrate
from django.dispatch import receiver
# Create your models here.

class AvatarSesion(models.Model):
    elemento = models.OneToOneField('Elemento', models.DO_NOTHING, primary_key=True)
    asigna_reim_alumno_sesion = models.ForeignKey('AsignaReimAlumno', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Avatar-Sesion'
        unique_together = (('elemento', 'asigna_reim_alumno_sesion'),)


class ElemAct(models.Model):
    elemento = models.OneToOneField('Elemento', models.DO_NOTHING, primary_key=True)
    actividad = models.ForeignKey('Actividad', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Elem-Act'
        unique_together = (('elemento', 'actividad'),)


class ElemReim(models.Model):
    elemento = models.OneToOneField('Elemento', models.DO_NOTHING, primary_key=True)
    reim = models.ForeignKey('Reim', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Elem-REIM'
        unique_together = (('elemento', 'reim'),)


class Fecha(models.Model):
    update_link = models.DateTimeField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'FECHA'


# class GrupoColegio(models.Model):
#     colegio_id_grupo = models.OneToOneField('Colegio', models.DO_NOTHING, db_column='colegio_id_Grupo', primary_key=True)  # Field name made lowercase.
#     colegio_id_colegio = models.ForeignKey('Colegio', models.DO_NOTHING, db_column='colegio_id_Colegio')  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'Grupo_Colegio'
#         unique_together = (('colegio_id_grupo', 'colegio_id_colegio'),)


class ReimAmbiente(models.Model):
    reim = models.OneToOneField('Reim', models.DO_NOTHING, primary_key=True)
    ambiente_id_ambiente = models.ForeignKey('Ambiente', models.DO_NOTHING, db_column='ambiente_id_ambiente')

    class Meta:
        managed = False
        db_table = 'REIM-Ambiente'
        unique_together = (('reim', 'ambiente_id_ambiente'),)


class Url(models.Model):
    id_ulearnet = models.IntegerField(primary_key=True)
    link = models.CharField(max_length=225)
    fecha_update_link = models.ForeignKey(Fecha, models.DO_NOTHING, db_column='FECHA_update_link')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'URL'


class Actividad(models.Model):
    nombre = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'actividad'


class ActividadOa(models.Model):
    id_oa = models.OneToOneField('ObjetivoAprendizaje', models.DO_NOTHING, db_column='id_oa', primary_key=True)
    id_actividad = models.ForeignKey(Actividad, models.DO_NOTHING, db_column='id_actividad')

    class Meta:
        managed = False
        db_table = 'actividad_oa'
        unique_together = (('id_oa', 'id_actividad'),)


class Actividadxreim(models.Model):
    id_actividad = models.OneToOneField(Actividad, models.DO_NOTHING, db_column='id_actividad', primary_key=True)
    id_reim = models.ForeignKey('Reim', models.DO_NOTHING, db_column='id_reim')

    class Meta:
        managed = False
        db_table = 'actividadxreim'
        unique_together = (('id_actividad', 'id_reim'),)


class Alternativa(models.Model):
    idlaternativa = models.IntegerField(primary_key=True)
    txt_alte = models.CharField(max_length=225)
    imagen_idimagen = models.ForeignKey('Imagen', models.DO_NOTHING, db_column='IMAGEN_idimagen', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'alternativa'


class AlumnoRespuestaActividad(models.Model):
    id_per = models.OneToOneField('Periodo', models.DO_NOTHING, db_column='id_per', primary_key=True)
    id_user = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_user')
    id_reim = models.ForeignKey('Reim', models.DO_NOTHING, db_column='id_reim')
    id_actividad = models.ForeignKey(Actividad, models.DO_NOTHING, db_column='id_actividad')
    id_elemento = models.ForeignKey('Elemento', models.DO_NOTHING, db_column='id_elemento')
    datetime_touch = models.DateTimeField()
    eje_x = models.FloatField(db_column='Eje_X')  # Field name made lowercase.
    eje_y = models.FloatField(db_column='Eje_Y')  # Field name made lowercase.
    eje_z = models.FloatField(db_column='Eje_Z')  # Field name made lowercase.
    correcta = models.IntegerField()
    resultado = models.CharField(max_length=225)
    tipo_registro = models.IntegerField(db_column='Tipo_Registro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'alumno_respuesta_actividad'
        unique_together = (('id_per', 'id_user', 'id_reim', 'id_actividad', 'id_elemento', 'datetime_touch'),)


class Ambiente(models.Model):
    id_ambiente = models.AutoField(primary_key=True)
    nombre_ambiente = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ambiente'


class Aprueba(models.Model):
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idusuario')
    idimagen = models.IntegerField()
    fecha_aprueba = models.DateTimeField()
    justificacion = models.CharField(max_length=225)
    esaprobado = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'aprueba'


class AsignaReim(models.Model):
    letra = models.OneToOneField('Letra', models.DO_NOTHING, primary_key=True)
    periodo = models.ForeignKey('Periodo', models.DO_NOTHING)
    reim = models.ForeignKey('Reim', models.DO_NOTHING)
    colegio = models.ForeignKey('Colegio', models.DO_NOTHING)
    nivel = models.ForeignKey('Nivel', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'asigna_reim'
        unique_together = (('letra', 'periodo', 'reim', 'colegio', 'nivel'),)


class AsignaReimAlumno(models.Model):
    sesion_id = models.CharField(primary_key=True, max_length=45)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    periodo = models.ForeignKey('Periodo', models.DO_NOTHING)
    reim = models.ForeignKey('Reim', models.DO_NOTHING)
    datetime_inicio = models.DateTimeField()
    datetime_termino = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'asigna_reim_alumno'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CatalogoReim(models.Model):
    id = models.IntegerField(primary_key=True)
    sesion = models.ForeignKey(AsignaReimAlumno, models.DO_NOTHING)
    id_elemento = models.ForeignKey('Elemento', models.DO_NOTHING, db_column='id_elemento')
    cantidad = models.IntegerField()
    precio = models.IntegerField(blank=True, null=True)
    datetime_realiza = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalogo_reim'


class Ciudad(models.Model):
    nombre = models.CharField(max_length=255)
    region = models.ForeignKey('Region', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ciudad'


class Colegio(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fono = models.CharField(max_length=255, blank=True, null=True)
    rbd = models.IntegerField(unique=True, blank=True, null=True)
    dgv_rbd = models.IntegerField(blank=True, null=True)
    mrun = models.IntegerField(blank=True, null=True)
    rut_sostenedor = models.IntegerField(blank=True, null=True)
    p_juridica = models.IntegerField(blank=True, null=True)
    rural = models.IntegerField(blank=True, null=True)
    comuna = models.ForeignKey('Comuna', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'colegio'


class Comuna(models.Model):
    nombre = models.CharField(max_length=255)
    ciudad = models.ForeignKey(Ciudad, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comuna'


class DetalleElemento(models.Model):
    id_elemento = models.OneToOneField('Elemento', models.DO_NOTHING, db_column='id_elemento', primary_key=True)
    descripcion = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'detalle_elemento'


class DetalleUsuario(models.Model):
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    id_reim = models.ForeignKey('Reim', models.DO_NOTHING, db_column='id_reim')
    identificador_personal = models.CharField(max_length=120)
    opciones_inicio = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'detalle_usuario'


class DibujoReim(models.Model):
    id_dibujo_reim = models.AutoField(primary_key=True)
    sesion = models.ForeignKey(AsignaReimAlumno, models.DO_NOTHING)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    reim = models.ForeignKey('Reim', models.DO_NOTHING)
    actividad = models.ForeignKey(Actividad, models.DO_NOTHING)
    imagen = models.TextField()

    class Meta:
        managed = False
        db_table = 'dibujo_reim'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'




class Eje(models.Model):
    id_eje = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'eje'


class Elemento(models.Model):
    nombre = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'elemento'

class EvaluacionPropuesta(models.Model):
    id_elemento = models.OneToOneField(Elemento, models.DO_NOTHING, db_column='id_elemento')
    id_usuario = models.ForeignKey('Usuario',models.DO_NOTHING, db_column='id_usuario',related_name='evaluacion_idAlumno')
    fecha_creacion = models.DateTimeField(primary_key=True)
    id_docente = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_docente',related_name='evaluacion_idDocente')
    fecha_evaluacion = models.DateTimeField(blank=True, null=True)
    evaluacion = models.CharField(max_length=255, blank=True, null=True)
    propuesta = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'evaluacion_propuesta'
        unique_together = (('id_elemento', 'id_usuario', 'id_docente', 'fecha_creacion'),)

class Forma(models.Model):
    sesion = models.CharField(max_length=45)
    alternativa_idlaternativa = models.ForeignKey(Alternativa, models.DO_NOTHING, db_column='ALTERNATIVA_idlaternativa')  # Field name made lowercase.
    item_iditem = models.ForeignKey('Item', models.DO_NOTHING, db_column='ITEM_IdItem')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'forma'


class Graficoxactividad(models.Model):
    id_actividad = models.OneToOneField(Actividad, models.DO_NOTHING, db_column='id_actividad', primary_key=True)
    embedurl = models.CharField(db_column='embedUrl', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'graficoxactividad'

class Imagen(models.Model):
    idimagen = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45)
    imagen = models.TextField()

    class Meta:
        managed = False
        db_table = 'imagen'


class InventarioReim(models.Model):
    sesion = models.ForeignKey(AsignaReimAlumno, models.DO_NOTHING)
    id_elemento = models.ForeignKey(Elemento, models.DO_NOTHING, db_column='id_elemento')
    cantidad = models.IntegerField()
    datetime_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'inventario_reim'


class Item(models.Model):
    iditem = models.IntegerField(db_column='IdItem', primary_key=True)  # Field name made lowercase.
    pregunta = models.CharField(db_column='Pregunta', max_length=255)  # Field name made lowercase.
    justificacion = models.CharField(db_column='Justificacion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dificultad = models.IntegerField(db_column='Dificultad', blank=True, null=True)  # Field name made lowercase.
    imagen_idimagen = models.ForeignKey(Imagen, models.DO_NOTHING, db_column='IMAGEN_idimagen', blank=True, null=True)  # Field name made lowercase.
    reim = models.ForeignKey('Reim', models.DO_NOTHING)
    objetivo_aprendizaje = models.ForeignKey('ObjetivoAprendizaje', models.DO_NOTHING)
    elemento = models.ForeignKey(Elemento, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item'


class ItemAlt(models.Model):
    indice = models.IntegerField(primary_key=True)
    idlaternativa = models.ForeignKey(Alternativa, models.DO_NOTHING, db_column='idlaternativa', blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True)
    escorrecto = models.CharField(max_length=45, blank=True, null=True)
    item_iditem = models.ForeignKey(Item, models.DO_NOTHING, db_column='ITEM_IdItem', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'item_alt'


class Letra(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'letra'


class Nivel(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nivel'


class ObjetivoAprendizaje(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    eje_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'objetivo_aprendizaje'


class Opinionxdibujo(models.Model):
    id_dibujo_reim = models.ForeignKey(DibujoReim, models.DO_NOTHING, db_column='id_dibujo_reim')
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    fecha_insert = models.DateTimeField()
    opinion = models.CharField(max_length=225)

    class Meta:
        managed = False
        db_table = 'opinionxdibujo'


class Pais(models.Model):
    nombre = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'pais'


class Periodo(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'periodo'


class Pertenece(models.Model):
    fecha = models.DateTimeField(primary_key=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING)
    nivel = models.ForeignKey(Nivel, models.DO_NOTHING)
    letra = models.ForeignKey(Letra, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pertenece'
        unique_together = (('fecha', 'usuario', 'colegio', 'nivel', 'letra'),)


class Reaccion(models.Model):
    idreaccion = models.IntegerField(primary_key=True)
    nombrereaccion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reaccion'


class Reaccionxdibujo(models.Model):
    idreaccion = models.ForeignKey(Reaccion, models.DO_NOTHING, db_column='idreaccion')
    iddibujo = models.ForeignKey(DibujoReim, models.DO_NOTHING, db_column='iddibujo')
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idusuario')
    fecha = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reaccionxdibujo'


class Region(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    pais = models.ForeignKey(Pais, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'region'


class Reim(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion_educativa = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'reim'


class SubEje(models.Model):
    id_sub_eje = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    id_eje = models.ForeignKey(Eje, models.DO_NOTHING, db_column='id_eje')

    class Meta:
        managed = False
        db_table = 'sub_eje'


class Tiempoxactividad(models.Model):
    inicio = models.DateTimeField(blank=True, null=True)
    final = models.DateTimeField(blank=True, null=True)
    causa = models.IntegerField()
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    reim = models.ForeignKey(Reim, models.DO_NOTHING)
    actividad = models.ForeignKey(Actividad, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tiempoxactividad'


class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_usuario'


# class TransaccionReim(models.Model):
#     usuarioenvia = models.ForeignKey('Usuario', models.DO_NOTHING)
#     usuariorecibe = models.ForeignKey('Usuario', models.DO_NOTHING)
#     elemento = models.ForeignKey(Elemento, models.DO_NOTHING)
#     catalogo = models.ForeignKey(CatalogoReim, models.DO_NOTHING, blank=True, null=True)
#     cantidad = models.IntegerField()
#     datetime_transac = models.DateTimeField()
#     estado = models.CharField(max_length=1)

#     class Meta:
#         managed = False
#         db_table = 'transaccion_reim'


class Usuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=255, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=255, blank=True, null=True)
    apellido_materno = models.CharField(max_length=255, blank=True, null=True)
    rut = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    alumno = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=128)
    password = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    nick_name = models.CharField(max_length=45, blank=True, null=True)
    tipo_usuario = models.ForeignKey(TipoUsuario, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'usuario'
