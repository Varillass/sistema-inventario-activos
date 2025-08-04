from django.db import models
from django.db.models import Max
from datetime import date
import re

# Create your models here.

class Sede(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.TextField(blank=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"

class Area(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Área"
        verbose_name_plural = "Áreas"

class Estado(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    # Información básica
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, help_text="Tipo de equipo (ej: Compresora, Motor, etc.)")
    numero_serie = models.CharField(max_length=20, unique=True, blank=True)
    observacion = models.TextField(blank=True, verbose_name="Observación", help_text="Observaciones adicionales sobre el equipo")
    
    # Información comercial
    marca = models.CharField(max_length=100, blank=True)
    modelo = models.CharField(max_length=100, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    proveedor = models.CharField(max_length=200, blank=True)
    fecha_compra = models.DateField(null=True, blank=True)
    garantia_hasta = models.DateField(null=True, blank=True)
    
    # Información de mantenimiento
    fecha_mantenimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Mantenimiento", help_text="Fecha del próximo mantenimiento programado")
    vida_util = models.IntegerField(null=True, blank=True, verbose_name="Vida Útil (años)", help_text="Vida útil estimada del equipo en años")
    
    # Relaciones
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='equipos', verbose_name="Sede", null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='equipos')
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='equipos')
    fecha_registro = models.DateField(auto_now_add=True)

    def _generar_prefijo(self):
        """Genera un prefijo de 3 letras basado en el tipo de equipo"""
        tipo_limpio = re.sub(r'[^a-zA-Z\s]', '', self.tipo)
        palabras = tipo_limpio.split()
        
        if len(palabras) >= 2:
            # Si hay 2 o más palabras, tomar primeras letras
            prefijo = ''.join([palabra[0].upper() for palabra in palabras[:3]])
        elif len(palabras) == 1 and len(palabras[0]) >= 3:
            # Si hay una palabra larga, tomar primeras 3 letras
            prefijo = palabras[0][:3].upper()
        else:
            # Fallback para casos especiales
            prefijo = (tipo_limpio[:3] + "XXX")[:3].upper()
        
        # Asegurar que tenga exactamente 3 caracteres
        return prefijo.ljust(3, 'X')[:3]

    def save(self, *args, **kwargs):
        if not self.numero_serie:
            prefijo = self._generar_prefijo()
            
            # Buscar el último número para este prefijo
            ultimo = Equipo.objects.filter(numero_serie__startswith=prefijo + '-').aggregate(
                Max('numero_serie'))['numero_serie__max']
            
            if ultimo:
                try:
                    # Extraer el número del formato "XXX-00001"
                    num = int(ultimo.split('-')[1]) + 1
                except (IndexError, ValueError):
                    num = 1
            else:
                num = 1
            
            self.numero_serie = f"{prefijo}-{num:05d}"
        super().save(*args, **kwargs)

    @property
    def garantia_vigente(self):
        if self.garantia_hasta:
            return self.garantia_hasta >= date.today()
        return False
    
    @property
    def mantenimiento_proximo(self):
        """Retorna True si el mantenimiento está programado para los próximos 30 días"""
        if self.fecha_mantenimiento:
            dias_restantes = (self.fecha_mantenimiento - date.today()).days
            return 0 <= dias_restantes <= 30
        return False
    
    @property
    def mantenimiento_vencido(self):
        """Retorna True si el mantenimiento está vencido"""
        if self.fecha_mantenimiento:
            return self.fecha_mantenimiento < date.today()
        return False

    def __str__(self):
        return f"{self.nombre} ({self.numero_serie})"

    class Meta:
        ordering = ['-fecha_registro']
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
