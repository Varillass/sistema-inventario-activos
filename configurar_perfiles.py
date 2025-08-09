#!/usr/bin/env python
"""
Script para configurar perfiles de usuario con permisos apropiados
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_activos.settings')
django.setup()

from django.contrib.auth.models import User
from inventario.models import PerfilUsuario

def configurar_perfiles():
    """Configura los perfiles de usuario con permisos apropiados"""
    
    print("🔧 Configurando perfiles de usuario...")
    
    # Obtener o crear usuarios
    usuarios = {
        'admin': {
            'username': 'admin',
            'email': 'admin@inventario.com',
            'password': 'admin123',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'rol': 'admin',
            'puede_eliminar': True,
            'puede_editar': True,
            'puede_crear': True,
            'puede_exportar': True,
            'puede_importar': True,
        },
        'supervisor': {
            'username': 'supervisor',
            'email': 'supervisor@inventario.com',
            'password': 'supervisor123',
            'first_name': 'Usuario',
            'last_name': 'Supervisor',
            'rol': 'supervisor',
            'puede_eliminar': True,
            'puede_editar': True,
            'puede_crear': True,
            'puede_exportar': True,
            'puede_importar': True,
        },
        'inventario': {
            'username': 'inventario',
            'email': 'inventario@empresa.com',
            'password': 'inventario123',
            'first_name': 'Usuario',
            'last_name': 'Inventario',
            'rol': 'usuario',
            'puede_eliminar': False,  # Los usuarios normales NO pueden eliminar
            'puede_editar': True,
            'puede_crear': True,
            'puede_exportar': True,
            'puede_importar': False,
        },
    }
    
    for username, datos in usuarios.items():
        # Crear o obtener usuario
        user, created = User.objects.get_or_create(
            username=datos['username'],
            defaults={
                'email': datos['email'],
                'first_name': datos['first_name'],
                'last_name': datos['last_name'],
            }
        )
        
        if created:
            user.set_password(datos['password'])
            user.save()
            print(f"✅ Usuario creado: {username}/{datos['password']}")
        else:
            print(f"ℹ️ Usuario existente: {username}")
        
        # Crear o actualizar perfil
        perfil, perfil_created = PerfilUsuario.objects.get_or_create(
            usuario=user,
            defaults={
                'rol': datos['rol'],
                'puede_eliminar': datos['puede_eliminar'],
                'puede_editar': datos['puede_editar'],
                'puede_crear': datos['puede_crear'],
                'puede_exportar': datos['puede_exportar'],
                'puede_importar': datos['puede_importar'],
            }
        )
        
        if not perfil_created:
            # Actualizar permisos existentes
            perfil.rol = datos['rol']
            perfil.puede_eliminar = datos['puede_eliminar']
            perfil.puede_editar = datos['puede_editar']
            perfil.puede_crear = datos['puede_crear']
            perfil.puede_exportar = datos['puede_exportar']
            perfil.puede_importar = datos['puede_importar']
            perfil.save()
            print(f"🔄 Perfil actualizado: {username}")
        else:
            print(f"✅ Perfil creado: {username}")
    
    print("\n📋 Resumen de permisos:")
    print("=" * 50)
    print("👑 ADMINISTRADOR (admin/admin123)")
    print("   - Puede crear, editar, eliminar, exportar e importar")
    print("   - Acceso completo al sistema")
    print()
    print("👨‍💼 SUPERVISOR (supervisor/supervisor123)")
    print("   - Puede crear, editar, eliminar, exportar e importar")
    print("   - Acceso completo al sistema")
    print()
    print("👤 USUARIO (inventario/inventario123)")
    print("   - Puede crear y editar equipos")
    print("   - Puede exportar datos")
    print("   - NO puede eliminar equipos")
    print("   - NO puede importar datos")
    print("=" * 50)
    print("\n🎉 Configuración completada exitosamente!")

if __name__ == '__main__':
    configurar_perfiles()
