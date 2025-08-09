#!/usr/bin/env python
"""
Script para probar que los permisos funcionan correctamente
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_activos.settings')
django.setup()

from django.contrib.auth.models import User
from inventario.models import PerfilUsuario, Equipo, Area, Estado, Sede

def probar_permisos():
    """Prueba los permisos de los diferentes usuarios"""
    
    print("🧪 Probando sistema de permisos...")
    print("=" * 50)
    
    # Obtener usuarios
    usuarios = ['admin', 'supervisor', 'inventario']
    
    for username in usuarios:
        try:
            user = User.objects.get(username=username)
            perfil = user.perfil
            
            print(f"\n👤 Usuario: {username}")
            print(f"   Rol: {perfil.get_rol_display()}")
            print(f"   Permisos:")
            print(f"   - Crear: {'✅' if perfil.puede_crear else '❌'}")
            print(f"   - Editar: {'✅' if perfil.puede_editar else '❌'}")
            print(f"   - Eliminar: {'✅' if perfil.puede_eliminar else '❌'}")
            print(f"   - Exportar: {'✅' if perfil.puede_exportar else '❌'}")
            print(f"   - Importar: {'✅' if perfil.puede_importar else '❌'}")
            
        except User.DoesNotExist:
            print(f"❌ Usuario {username} no existe")
        except PerfilUsuario.DoesNotExist:
            print(f"❌ Perfil de {username} no existe")
    
    print("\n" + "=" * 50)
    print("📊 Estadísticas del sistema:")
    
    # Contar equipos
    total_equipos = Equipo.objects.count()
    print(f"   Total de equipos: {total_equipos}")
    
    # Contar usuarios con perfiles
    total_perfiles = PerfilUsuario.objects.count()
    print(f"   Total de perfiles: {total_perfiles}")
    
    # Contar por roles
    roles = PerfilUsuario.objects.values('rol').annotate(
        total=django.db.models.Count('rol')
    )
    print("   Distribución por roles:")
    for rol in roles:
        print(f"   - {rol['rol']}: {rol['total']} usuarios")
    
    print("\n✅ Prueba completada!")

if __name__ == '__main__':
    probar_permisos()
