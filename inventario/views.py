from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
from .models import Equipo, Estado, Area
from django.db.models import Count
# from .utils import generar_pdf_equipos  # Comentado temporalmente para evitar errores de reportlab

# Create your views here.

@login_required
def dashboard(request):
    # Totales por estado
    estados = Estado.objects.all()
    total_por_estado = []
    for estado in estados:
        total_por_estado.append({
            'nombre': estado.nombre,
            'total': Equipo.objects.filter(estado=estado).count()
        })

    # Áreas con más equipos
    areas = Area.objects.annotate(total_equipos=Count('equipos')).order_by('-total_equipos')[:5]

    context = {
        'total_por_estado': total_por_estado,
        'areas': areas,
        'total_equipos': Equipo.objects.count(),
    }
    return render(request, 'inventario/dashboard.html', context)

@login_required
def equipos_lista(request):
    equipos = Equipo.objects.all().select_related('area', 'estado')
    
    context = {
        'equipos': equipos,
        'areas': Area.objects.all(),
        'estados': Estado.objects.all(),
    }
    return render(request, 'inventario/equipos_lista.html', context)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def crear_equipo(request):
    try:
        data = json.loads(request.body)
        
        # Validar campos requeridos
        required_fields = ['nombre', 'tipo', 'area', 'estado']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'El campo {field} es requerido'
                }, status=400)
        
        # Crear el equipo
        equipo = Equipo.objects.create(
            nombre=data['nombre'],
            tipo=data['tipo'],
            numero_serie=data.get('numero_serie', ''),  # Se generará automáticamente si está vacío
            observacion=data.get('observacion', ''),
            area_id=data['area'],
            estado_id=data['estado']
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Equipo creado exitosamente',
            'equipo': {
                'id': equipo.id,
                'nombre': equipo.nombre,
                'numero_serie': equipo.numero_serie,
                'tipo': equipo.tipo,
                'area': equipo.area.nombre,
                'estado': equipo.estado.nombre
            }
        })
        
    except Area.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'El área seleccionada no existe'
        }, status=400)
        
    except Estado.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'El estado seleccionado no existe'
        }, status=400)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        }, status=400)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
@login_required
def obtener_equipo(request, equipo_id):
    try:
        equipo = get_object_or_404(Equipo, id=equipo_id)
        
        return JsonResponse({
            'success': True,
            'equipo': {
                'id': equipo.id,
                'nombre': equipo.nombre,
                'tipo': equipo.tipo,
                'numero_serie': equipo.numero_serie,
                'observacion': equipo.observacion,
                'area': equipo.area.id,
                'estado': equipo.estado.id,
                'marca': getattr(equipo, 'marca', ''),
                'modelo': getattr(equipo, 'modelo', ''),
                'precio': str(equipo.precio) if equipo.precio else '',
                'proveedor': getattr(equipo, 'proveedor', ''),
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al obtener el equipo: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def editar_equipo(request, equipo_id):
    try:
        equipo = get_object_or_404(Equipo, id=equipo_id)
        data = json.loads(request.body)
        
        # Validar campos requeridos
        required_fields = ['nombre', 'tipo', 'area', 'estado']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'El campo {field} es requerido'
                }, status=400)
        
        # Actualizar el equipo
        equipo.nombre = data['nombre']
        equipo.tipo = data['tipo']
        equipo.observacion = data.get('observacion', '')
        equipo.area_id = data['area']
        equipo.estado_id = data['estado']
        
        # Solo actualizar número de serie si se proporciona uno diferente
        if data.get('numero_serie') and data['numero_serie'] != equipo.numero_serie:
            # Validar que el nuevo número de serie no exista
            if Equipo.objects.filter(numero_serie=data['numero_serie']).exclude(id=equipo.id).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'El número de serie ya existe'
                }, status=400)
            equipo.numero_serie = data['numero_serie']
        
        equipo.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Equipo actualizado exitosamente',
            'equipo': {
                'id': equipo.id,
                'nombre': equipo.nombre,
                'numero_serie': equipo.numero_serie,
                'tipo': equipo.tipo,
                'area': equipo.area.nombre,
                'estado': equipo.estado.nombre
            }
        })
        
    except Area.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'El área seleccionada no existe'
        }, status=400)
        
    except Estado.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'El estado seleccionado no existe'
        }, status=400)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        }, status=400)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def eliminar_equipo(request, equipo_id):
    try:
        equipo = get_object_or_404(Equipo, id=equipo_id)
        nombre_equipo = equipo.nombre
        numero_serie = equipo.numero_serie
        
        equipo.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Equipo "{nombre_equipo}" ({numero_serie}) eliminado exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al eliminar el equipo: {str(e)}'
        }, status=500)

@login_required
def exportar_equipos_pdf(request):
    """
    Vista para exportar equipos a PDF - TEMPORALMENTE DESHABILITADA
    """
    return JsonResponse({
        'success': False,
        'error': 'La exportación PDF está temporalmente deshabilitada. Funcionalidad disponible próximamente.'
    }, status=503)

@login_required
def descargar_plantilla_excel(request):
    """
    Vista para descargar plantilla Excel - TEMPORALMENTE DESHABILITADA
    """
    return JsonResponse({
        'success': False,
        'error': 'La descarga de plantilla Excel está temporalmente deshabilitada. Funcionalidad disponible próximamente.'
    }, status=503)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def importar_equipos_excel(request):
    """
    Vista para importar equipos desde Excel - TEMPORALMENTE DESHABILITADA
    """
    return JsonResponse({
        'success': False,
        'error': 'La importación de Excel está temporalmente deshabilitada. Funcionalidad disponible próximamente.'
    }, status=503)
