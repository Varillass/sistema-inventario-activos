# 🔐 Sistema de Permisos de Usuario

## 📋 Descripción General

Se ha implementado un sistema completo de permisos de usuario para el Sistema de Inventario de Activos. Este sistema permite controlar qué acciones puede realizar cada usuario según su rol asignado.

## 👥 Roles de Usuario

### 👑 Administrador
- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Permisos:** Acceso completo al sistema
  - ✅ Crear equipos
  - ✅ Editar equipos
  - ✅ Eliminar equipos
  - ✅ Exportar datos
  - ✅ Importar datos

### 👨‍💼 Supervisor
- **Usuario:** `supervisor`
- **Contraseña:** `supervisor123`
- **Permisos:** Acceso completo al sistema
  - ✅ Crear equipos
  - ✅ Editar equipos
  - ✅ Eliminar equipos
  - ✅ Exportar datos
  - ✅ Importar datos

### 👤 Usuario
- **Usuario:** `inventario`
- **Contraseña:** `inventario123`
- **Permisos:** Acceso limitado
  - ✅ Crear equipos
  - ✅ Editar equipos
  - ❌ **NO puede eliminar equipos**
  - ✅ Exportar datos
  - ❌ **NO puede importar datos**

## 🏗️ Arquitectura del Sistema

### Modelo PerfilUsuario
```python
class PerfilUsuario(models.Model):
    ROLES_CHOICES = [
        ('admin', 'Administrador'),
        ('supervisor', 'Supervisor'),
        ('usuario', 'Usuario'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES_CHOICES, default='usuario')
    puede_eliminar = models.BooleanField(default=False)
    puede_editar = models.BooleanField(default=True)
    puede_crear = models.BooleanField(default=True)
    puede_exportar = models.BooleanField(default=True)
    puede_importar = models.BooleanField(default=False)
```

### Decoradores de Permisos
- `@requiere_permiso('crear')` - Verifica permiso de creación
- `@requiere_permiso('editar')` - Verifica permiso de edición
- `@requiere_permiso('eliminar')` - Verifica permiso de eliminación
- `@requiere_permiso('exportar')` - Verifica permiso de exportación
- `@requiere_permiso('importar')` - Verifica permiso de importación

### Middleware
- `PerfilUsuarioMiddleware` - Asegura que todos los usuarios tengan un perfil

## 🔧 Configuración

### 1. Ejecutar Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Configurar Perfiles
```bash
python configurar_perfiles.py
```

### 3. Probar Sistema
```bash
python probar_permisos.py
```

## 🎯 Funcionalidades Implementadas

### ✅ Control de Acceso
- Verificación de permisos en todas las vistas críticas
- Redirección automática si no hay permisos
- Mensajes de error informativos

### ✅ Interfaz Adaptativa
- Botones se muestran/ocultan según permisos
- Información del rol visible en la interfaz
- Badges indicativos del rol del usuario

### ✅ Seguridad
- Verificación tanto en frontend como backend
- Middleware para crear perfiles automáticamente
- Decoradores reutilizables

## 📱 Interfaz de Usuario

### Indicadores Visuales
- **Badge de rol** en el header principal
- **Botones condicionales** en la lista de equipos
- **Acciones limitadas** según permisos

### Comportamiento por Rol

#### Usuario Normal (inventario)
- ✅ Ve botón "Agregar Equipo"
- ✅ Ve botón "Exportar PDF/Excel"
- ❌ **NO ve botón "Eliminar"** en cada equipo
- ❌ **NO ve botones de importación**

#### Administrador/Supervisor
- ✅ Ve todos los botones
- ✅ Acceso completo a todas las funciones

## 🛠️ Administración

### Panel de Administración
- Acceso: `/admin/`
- Gestión de perfiles de usuario
- Configuración granular de permisos

### Scripts de Utilidad
- `configurar_perfiles.py` - Configuración inicial
- `probar_permisos.py` - Verificación del sistema

## 🔒 Seguridad

### Niveles de Protección
1. **Frontend** - Botones ocultos según permisos
2. **Backend** - Decoradores verifican permisos
3. **Middleware** - Perfiles automáticos
4. **Base de datos** - Permisos persistentes

### Validaciones
- Verificación en cada solicitud HTTP
- Respuestas JSON para AJAX
- Redirecciones para navegación normal
- Mensajes de error informativos

## 📈 Beneficios

### Para la Empresa
- **Control granular** de acceso
- **Auditoría** de acciones por usuario
- **Seguridad** mejorada
- **Escalabilidad** del sistema

### Para los Usuarios
- **Interfaz clara** de permisos
- **Feedback inmediato** sobre restricciones
- **Experiencia consistente** según rol

## 🚀 Próximas Mejoras

### Funcionalidades Adicionales
- [ ] Logs de auditoría
- [ ] Permisos por área/sede
- [ ] Roles personalizados
- [ ] Notificaciones de permisos

### Mejoras Técnicas
- [ ] Cache de permisos
- [ ] API de permisos
- [ ] Tests automatizados
- [ ] Documentación API

## 📞 Soporte

Para cualquier consulta sobre el sistema de permisos:
- Revisar logs del sistema
- Verificar configuración en `/admin/`
- Ejecutar `python probar_permisos.py`

---

**🎉 Sistema de permisos implementado exitosamente!**
