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
    # Función para asignar colores según el estado
    def get_estado_color(estado_nombre):
        estado_colors = {
            'Operativo': 'success',      # Verde
            'Bueno': 'success',          # Verde
            'Nuevo': 'info',             # Azul
            'Regular': 'warning',        # Amarillo
            'Mantenimiento': 'warning',  # Amarillo
            'En Reparación': 'warning',  # Amarillo
            'Malo': 'danger',            # Rojo
            'Inoperativo': 'danger',     # Rojo
            'Fuera de Servicio': 'danger', # Rojo
            'Dado de Baja': 'secondary', # Gris
            'En Almacén': 'info',        # Azul
        }
        return estado_colors.get(estado_nombre, 'primary')
    
    def get_estado_icon(estado_nombre):
        estado_icons = {
            'Operativo': 'fa-check-circle',
            'Bueno': 'fa-check-circle',
            'Nuevo': 'fa-star',
            'Regular': 'fa-exclamation-triangle',
            'Mantenimiento': 'fa-tools',
            'En Reparación': 'fa-wrench',
            'Malo': 'fa-times-circle',
            'Inoperativo': 'fa-times-circle',
            'Fuera de Servicio': 'fa-ban',
            'Dado de Baja': 'fa-trash',
            'En Almacén': 'fa-box',
        }
        return estado_icons.get(estado_nombre, 'fa-question-circle')
    
    # Totales por estado con colores e iconos
    estados = Estado.objects.all()
    total_por_estado = []
    for estado in estados:
        total_por_estado.append({
            'nombre': estado.nombre,
            'total': Equipo.objects.filter(estado=estado).count(),
            'color': get_estado_color(estado.nombre),
            'icon': get_estado_icon(estado.nombre)
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
        
        # Debug: Imprimir los datos recibidos
        print("Datos recibidos:", data)
        
        # Validar campos requeridos
        required_fields = ['nombre', 'tipo', 'area', 'estado']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'El campo {field} es requerido'
                }, status=400)
        
        # Procesar campos opcionales
        precio = data.get('precio')
        if precio == '' or precio is None:
            precio = None
        elif precio:
            try:
                precio = float(precio)
            except (ValueError, TypeError):
                precio = None
        
        fecha_compra = data.get('fecha_compra')
        if fecha_compra == '' or fecha_compra is None:
            fecha_compra = None
            
        garantia_hasta = data.get('garantia_hasta')
        if garantia_hasta == '' or garantia_hasta is None:
            garantia_hasta = None
        
        # Crear el equipo
        equipo = Equipo.objects.create(
            nombre=data['nombre'],
            tipo=data['tipo'],
            numero_serie=data.get('numero_serie', ''),
            marca=data.get('marca', ''),
            modelo=data.get('modelo', ''),
            precio=precio,
            proveedor=data.get('proveedor', ''),
            fecha_compra=fecha_compra,
            garantia_hasta=garantia_hasta,
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
                'fecha_compra': equipo.fecha_compra.strftime('%Y-%m-%d') if equipo.fecha_compra else '',
                'garantia_hasta': equipo.garantia_hasta.strftime('%Y-%m-%d') if equipo.garantia_hasta else '',
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
        
        # Procesar campos opcionales
        precio = data.get('precio')
        if precio == '' or precio is None:
            precio = None
        elif precio:
            try:
                precio = float(precio)
            except (ValueError, TypeError):
                precio = None
        
        fecha_compra = data.get('fecha_compra')
        if fecha_compra == '' or fecha_compra is None:
            fecha_compra = None
            
        garantia_hasta = data.get('garantia_hasta')
        if garantia_hasta == '' or garantia_hasta is None:
            garantia_hasta = None
        
        # Actualizar el equipo
        equipo.nombre = data['nombre']
        equipo.tipo = data['tipo']
        equipo.marca = data.get('marca', '')
        equipo.modelo = data.get('modelo', '')
        equipo.precio = precio
        equipo.proveedor = data.get('proveedor', '')
        equipo.fecha_compra = fecha_compra
        equipo.garantia_hasta = garantia_hasta
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
    Vista para exportar equipos a PDF
    """
    try:
        # Obtener todos los equipos con sus relaciones
        equipos = Equipo.objects.all().select_related('area', 'estado').order_by('numero_serie')
        
        # Generar PDF
        from .utils import generar_pdf_equipos
        pdf_content = generar_pdf_equipos(equipos)
        
        # Crear respuesta HTTP
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="inventario_activos.pdf"'
        
        return response
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al generar PDF: {str(e)}'
        }, status=500)

@login_required
def exportar_equipos_excel(request):
    """
    Vista para exportar equipos a Excel
    """
    try:
        # Obtener todos los equipos con sus relaciones
        equipos = Equipo.objects.all().select_related('area', 'estado').order_by('numero_serie')
        
        # Generar Excel
        from .utils import generar_excel_equipos
        excel_content = generar_excel_equipos(equipos)
        
        # Crear respuesta HTTP
        response = HttpResponse(excel_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="inventario_activos.xlsx"'
        
        return response
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al generar Excel: {str(e)}'
        }, status=500)

@login_required
def descargar_plantilla_excel(request):
    """
    Vista para descargar plantilla Excel
    """
    try:
        from .utils import generar_plantilla_excel
        excel_content = generar_plantilla_excel()
        
        response = HttpResponse(excel_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="plantilla_importacion_equipos.xlsx"'
        
        return response
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al generar plantilla Excel: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def importar_equipos_excel(request):
    """
    Vista para importar equipos desde Excel
    """
    try:
        if 'archivo' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'No se ha seleccionado ningún archivo'
            }, status=400)
        
        archivo = request.FILES['archivo']
        
        # Validar archivo
        from .utils import validar_archivo_excel, procesar_importacion_excel
        es_valido, mensaje = validar_archivo_excel(archivo)
        
        if not es_valido:
            return JsonResponse({
                'success': False,
                'error': mensaje
            }, status=400)
        
        # Procesar importación
        equipos_creados, errores = procesar_importacion_excel(archivo)
        
        # Preparar respuesta
        if equipos_creados > 0:
            mensaje = f'Se importaron {equipos_creados} equipos exitosamente'
            if errores:
                mensaje += f'. Se encontraron {len(errores)} errores'
            
            return JsonResponse({
                'success': True,
                'message': mensaje,
                'equipos_creados': equipos_creados,
                'errores': errores
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'No se pudo importar ningún equipo. Verifica el formato del archivo.',
                'errores': errores
            }, status=400)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al procesar el archivo: {str(e)}'
        }, status=500)
