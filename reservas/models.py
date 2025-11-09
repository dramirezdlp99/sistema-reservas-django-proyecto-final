from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class TipoEspacio(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    capacidad_minima = models.IntegerField(default=1)
    capacidad_maxima = models.IntegerField(default=100)
    
    class Meta:
        verbose_name = 'Tipo de Espacio'
        verbose_name_plural = 'Tipos de Espacios'
    
    def __str__(self):
        return self.nombre

class Espacio(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoEspacio, on_delete=models.CASCADE, related_name='espacios')
    codigo = models.CharField(max_length=20, unique=True)
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    equipamiento = models.TextField(blank=True, help_text="Lista de equipos disponibles")
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='espacios/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Espacio'
        verbose_name_plural = 'Espacios'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE, related_name='reservas')
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    motivo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    confirmacion_automatica = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    confirmada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservas_confirmadas')
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-fecha_reserva', '-hora_inicio']
    
    def __str__(self):
        return f"{self.espacio.codigo} - {self.fecha_reserva} {self.hora_inicio}"
    
    def clean(self):
        # Validar que la fecha no sea pasada
        if self.fecha_reserva < timezone.now().date():
            raise ValidationError('No se puede reservar en fechas pasadas')
        
        # Validar que hora_fin sea mayor que hora_inicio
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError('La hora de fin debe ser posterior a la hora de inicio')
        
        # Validar conflictos de horario
        conflictos = Reserva.objects.filter(
            espacio=self.espacio,
            fecha_reserva=self.fecha_reserva,
            estado__in=['PENDIENTE', 'CONFIRMADA']
        ).exclude(pk=self.pk)
        
        for reserva in conflictos:
            # Verificar solapamiento de horarios
            if (self.hora_inicio < reserva.hora_fin and self.hora_fin > reserva.hora_inicio):
                raise ValidationError(
                    f'El espacio ya está reservado de {reserva.hora_inicio} a {reserva.hora_fin}'
                )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if self.confirmacion_automatica and self.estado == 'PENDIENTE':
            self.estado = 'CONFIRMADA'
        super().save(*args, **kwargs)

class PerfilUsuario(models.Model):
    ROLES = [
        ('USUARIO', 'Usuario'),
        ('ADMINISTRADOR', 'Administrador'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='USUARIO')
    telefono = models.CharField(max_length=20, blank=True)
    departamento = models.CharField(max_length=100, blank=True)
    notificaciones_email = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'
    
    def __str__(self):
        return f"{self.user.username} - {self.rol}"