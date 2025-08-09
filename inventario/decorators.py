from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from functools import wraps
from django.contrib.auth.decorators import login_required

def requiere_permiso(permiso):
    """
    Decorador para verificar si un usuario tiene un permiso específico
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            # Obtener el perfil del usuario
            try:
                perfil = request.user.perfil
            except:
                # Si no existe perfil, crear uno por defecto
                from .models import PerfilUsuario
                perfil = PerfilUsuario.objects.create(usuario=request.user)
            
            # Verificar el permiso específico
            if permiso == 'eliminar' and not perfil.puede_eliminar:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': 'No tienes permisos para eliminar equipos'
                    }, status=403)
                else:
                    messages.error(request, 'No tienes permisos para eliminar equipos')
                    return redirect('equipos_lista')
            
            elif permiso == 'editar' and not perfil.puede_editar:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': 'No tienes permisos para editar equipos'
                    }, status=403)
                else:
                    messages.error(request, 'No tienes permisos para editar equipos')
                    return redirect('equipos_lista')
            
            elif permiso == 'crear' and not perfil.puede_crear:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': 'No tienes permisos para crear equipos'
                    }, status=403)
                else:
                    messages.error(request, 'No tienes permisos para crear equipos')
                    return redirect('equipos_lista')
            
            elif permiso == 'exportar' and not perfil.puede_exportar:
                messages.error(request, 'No tienes permisos para exportar datos')
                return redirect('equipos_lista')
            
            elif permiso == 'importar' and not perfil.puede_importar:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': 'No tienes permisos para importar datos'
                    }, status=403)
                else:
                    messages.error(request, 'No tienes permisos para importar datos')
                    return redirect('equipos_lista')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def requiere_rol(roles):
    """
    Decorador para verificar si un usuario tiene un rol específico
    """
    if isinstance(roles, str):
        roles = [roles]
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            # Obtener el perfil del usuario
            try:
                perfil = request.user.perfil
            except:
                # Si no existe perfil, crear uno por defecto
                from .models import PerfilUsuario
                perfil = PerfilUsuario.objects.create(usuario=request.user)
            
            # Verificar si el usuario tiene uno de los roles requeridos
            if perfil.rol not in roles:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': 'No tienes permisos suficientes para realizar esta acción'
                    }, status=403)
                else:
                    messages.error(request, 'No tienes permisos suficientes para realizar esta acción')
                    return redirect('equipos_lista')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
