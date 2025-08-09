from django.shortcuts import redirect
from .models import PerfilUsuario

class PerfilUsuarioMiddleware:
    """
    Middleware para asegurar que todos los usuarios autenticados tengan un perfil
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Procesar la solicitud
        response = self.get_response(request)
        
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            try:
                # Intentar obtener el perfil del usuario
                perfil = request.user.perfil
            except PerfilUsuario.DoesNotExist:
                # Si no existe perfil, crear uno por defecto
                perfil = PerfilUsuario.objects.create(
                    usuario=request.user,
                    rol='usuario',  # Rol por defecto
                    puede_eliminar=False,  # Por defecto no puede eliminar
                    puede_editar=True,
                    puede_crear=True,
                    puede_exportar=True,
                    puede_importar=False,
                )
        
        return response
