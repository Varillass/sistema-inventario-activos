from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
from django.db.models import Count
from .models import Equipo, Area, Estado
import pandas as pd
import re

def generar_pdf_equipos(filtro_area=None, filtro_estado=None, filtro_tipo=None):
    """
    Genera un PDF profesional con el listado de equipos
    """
    buffer = BytesIO()
    
    # Configuración del documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#34495e'),
        fontName='Helvetica-Bold'
    )
    
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=10,
        alignment=TA_RIGHT,
        textColor=colors.HexColor('#7f8c8d')
    )
    
    # Contenido del PDF
    story = []
    
    # Encabezado
    title = Paragraph("INVENTARIO DE ACTIVOS", title_style)
    story.append(title)
    
    # Información del reporte
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    info_reporte = f"Fecha de generación: {fecha_actual}"
    story.append(Paragraph(info_reporte, info_style))
    story.append(Spacer(1, 20))
    
    # Filtros aplicados
    filtros_aplicados = []
    if filtro_area and filtro_area != 'todas':
        try:
            area = Area.objects.get(id=filtro_area)
            filtros_aplicados.append(f"Área: {area.nombre}")
        except Area.DoesNotExist:
            pass
    
    if filtro_estado and filtro_estado != 'todos':
        try:
            estado = Estado.objects.get(id=filtro_estado)
            filtros_aplicados.append(f"Estado: {estado.nombre}")
        except Estado.DoesNotExist:
            pass
    
    if filtro_tipo and filtro_tipo != 'todos':
        filtros_aplicados.append(f"Tipo: {filtro_tipo}")
    
    if filtros_aplicados:
        story.append(Paragraph("FILTROS APLICADOS", subtitle_style))
        for filtro in filtros_aplicados:
            story.append(Paragraph(f"• {filtro}", styles['Normal']))
        story.append(Spacer(1, 20))
    
    # Obtener equipos según filtros
    equipos = Equipo.objects.all()
    
    if filtro_area and filtro_area != 'todas':
        equipos = equipos.filter(area_id=filtro_area)
    
    if filtro_estado and filtro_estado != 'todos':
        equipos = equipos.filter(estado_id=filtro_estado)
    
    if filtro_tipo and filtro_tipo != 'todos':
        equipos = equipos.filter(tipo__icontains=filtro_tipo)
    
    equipos = equipos.select_related('area', 'estado').order_by('numero_serie')
    
    # Resumen estadístico
    total_equipos = equipos.count()
    story.append(Paragraph("RESUMEN", subtitle_style))
    story.append(Paragraph(f"Total de equipos: {total_equipos}", styles['Normal']))
    
    # Estadísticas por área
    stats_area = equipos.values('area__nombre').annotate(total=Count('id')).order_by('-total')
    if stats_area:
        story.append(Paragraph("<br/>Distribución por área:", styles['Normal']))
        for stat in stats_area:
            story.append(Paragraph(f"• {stat['area__nombre']}: {stat['total']} equipos", styles['Normal']))
    
    # Estadísticas por estado
    stats_estado = equipos.values('estado__nombre').annotate(total=Count('id')).order_by('-total')
    if stats_estado:
        story.append(Paragraph("<br/>Distribución por estado:", styles['Normal']))
        for stat in stats_estado:
            story.append(Paragraph(f"• {stat['estado__nombre']}: {stat['total']} equipos", styles['Normal']))
    
    story.append(Spacer(1, 30))
    
    # Tabla de equipos
    story.append(Paragraph("LISTADO DETALLADO DE EQUIPOS", subtitle_style))
    
    # Encabezados de la tabla
    data = [
        ['N° Serie', 'Tipo', 'Marca', 'Modelo', 'Área', 'Estado', 'Precio']
    ]
    
    # Datos de equipos
    for equipo in equipos:
        precio_formato = f"${equipo.precio:,.2f}" if equipo.precio else "N/A"
        data.append([
            equipo.numero_serie,
            equipo.tipo,
            equipo.marca or "N/A",
            equipo.modelo or "N/A",
            equipo.area.nombre,
            equipo.estado.nombre,
            precio_formato
        ])
    
    # Crear tabla
    table = Table(data, colWidths=[1.2*inch, 1*inch, 1*inch, 1*inch, 1*inch, 0.8*inch, 0.8*inch])
    
    # Estilo de la tabla
    table.setStyle(TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        
        # Contenido
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        
        # Bordes
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        
        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.lightgrey]),
        
        # Espaciado
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(table)
    
    # Pie de página
    story.append(Spacer(1, 50))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#95a5a6')
    )
    
    story.append(Paragraph("Sistema de Inventario de Activos - Reporte Generado Automáticamente", footer_style))
    story.append(Paragraph(f"Página generada el {fecha_actual}", footer_style))
    
    # Construir PDF
    doc.build(story)
    
    # Obtener el PDF
    buffer.seek(0)
    return buffer 

def validar_archivo_excel(archivo):
    """
    Valida que el archivo sea un Excel válido
    """
    try:
        # Verificar extensión
        nombre = archivo.name.lower()
        if not (nombre.endswith('.xlsx') or nombre.endswith('.xls') or nombre.endswith('.csv')):
            return False, "El archivo debe ser .xlsx, .xls o .csv"
        
        # Intentar leer el archivo
        if nombre.endswith('.csv'):
            df = pd.read_csv(archivo)
        else:
            df = pd.read_excel(archivo)
        
        # Verificar que no esté vacío
        if df.empty:
            return False, "El archivo está vacío"
        
        return True, df
        
    except Exception as e:
        return False, f"Error al leer el archivo: {str(e)}"

def procesar_importacion_excel(archivo):
    """
    Procesa la importación masiva desde Excel
    """
    # Validar archivo
    es_valido, resultado = validar_archivo_excel(archivo)
    if not es_valido:
        return False, resultado, []
    
    df = resultado
    
    # Mapeo de columnas esperadas (sin distinguir mayúsculas)
    columnas_requeridas = {
        'nombre': ['nombre', 'name', 'equipo', 'equipment'],
        'tipo': ['tipo', 'type', 'categoria', 'category'],
        'area': ['area', 'área', 'departamento', 'department'],
        'estado': ['estado', 'status', 'condition'],
    }
    
    columnas_opcionales = {
        'marca': ['marca', 'brand', 'fabricante', 'manufacturer'],
        'modelo': ['modelo', 'model'],
        'precio': ['precio', 'price', 'cost', 'costo', 'valor', 'value'],
        'proveedor': ['proveedor', 'supplier', 'vendor'],
        'observacion': ['observacion', 'observación', 'descripcion', 'descripción', 'description', 'notes', 'notas'],
        'fecha_compra': ['fecha_compra', 'fecha compra', 'purchase_date', 'date_purchased', 'compra'],
        'garantia_hasta': ['garantia_hasta', 'garantía hasta', 'warranty_until', 'garantia', 'garantía']
    }
    
    # Normalizar nombres de columnas del DataFrame
    df.columns = df.columns.str.lower().str.strip()
    
    # Mapear columnas del archivo a nuestros campos
    mapeo_columnas = {}
    
    # Buscar columnas requeridas
    for campo, posibles_nombres in columnas_requeridas.items():
        encontrada = False
        for col in df.columns:
            if any(nombre in col for nombre in posibles_nombres):
                mapeo_columnas[campo] = col
                encontrada = True
                break
        
        if not encontrada:
            return False, f"Columna requerida '{campo}' no encontrada. Busque: {', '.join(posibles_nombres)}", []
    
    # Buscar columnas opcionales
    for campo, posibles_nombres in columnas_opcionales.items():
        for col in df.columns:
            if any(nombre in col for nombre in posibles_nombres):
                mapeo_columnas[campo] = col
                break
    
    # Procesar datos
    equipos_procesados = []
    errores = []
    
    for index, row in df.iterrows():
        try:
            fila_num = index + 2  # +2 porque index empieza en 0 y primera fila son headers
            
            # Extraer datos requeridos
            nombre = str(row[mapeo_columnas['nombre']]).strip()
            tipo = str(row[mapeo_columnas['tipo']]).strip()
            area_nombre = str(row[mapeo_columnas['area']]).strip()
            estado_nombre = str(row[mapeo_columnas['estado']]).strip()
            
            # Validar datos requeridos
            if not nombre or nombre == 'nan':
                errores.append(f"Fila {fila_num}: Nombre es requerido")
                continue
            
            if not tipo or tipo == 'nan':
                errores.append(f"Fila {fila_num}: Tipo es requerido")
                continue
            
            # Buscar o crear área
            try:
                area = Area.objects.get(nombre__iexact=area_nombre)
            except Area.DoesNotExist:
                area = Area.objects.create(nombre=area_nombre)
            
            # Buscar o crear estado
            try:
                estado = Estado.objects.get(nombre__iexact=estado_nombre)
            except Estado.DoesNotExist:
                estado = Estado.objects.create(nombre=estado_nombre)
            
            # Datos opcionales
            marca = row.get(mapeo_columnas.get('marca', ''), '')
            if pd.isna(marca):
                marca = ''
            else:
                marca = str(marca).strip()
            
            modelo = row.get(mapeo_columnas.get('modelo', ''), '')
            if pd.isna(modelo):
                modelo = ''
            else:
                modelo = str(modelo).strip()
            
            # Precio
            precio = None
            if 'precio' in mapeo_columnas:
                precio_val = row.get(mapeo_columnas['precio'], '')
                if not pd.isna(precio_val) and precio_val != '':
                    try:
                        # Limpiar formato de precio (quitar $, comas, etc.)
                        precio_str = str(precio_val).replace('$', '').replace(',', '').strip()
                        precio = float(precio_str)
                    except (ValueError, TypeError):
                        errores.append(f"Fila {fila_num}: Precio inválido '{precio_val}'")
            
            # Proveedor
            proveedor = ''
            if 'proveedor' in mapeo_columnas:
                prov_val = row.get(mapeo_columnas['proveedor'], '')
                if not pd.isna(prov_val):
                    proveedor = str(prov_val).strip()
            
            # Observación
            observacion = ''
            if 'observacion' in mapeo_columnas:
                obs_val = row.get(mapeo_columnas['observacion'], '')
                if not pd.isna(obs_val):
                    observacion = str(obs_val).strip()
            
            # Fechas
            fecha_compra = None
            if 'fecha_compra' in mapeo_columnas:
                fecha_val = row.get(mapeo_columnas['fecha_compra'], '')
                if not pd.isna(fecha_val) and fecha_val != '':
                    try:
                        fecha_compra = pd.to_datetime(fecha_val).date()
                    except:
                        errores.append(f"Fila {fila_num}: Fecha de compra inválida '{fecha_val}'")
            
            garantia_hasta = None
            if 'garantia_hasta' in mapeo_columnas:
                garantia_val = row.get(mapeo_columnas['garantia_hasta'], '')
                if not pd.isna(garantia_val) and garantia_val != '':
                    try:
                        garantia_hasta = pd.to_datetime(garantia_val).date()
                    except:
                        errores.append(f"Fila {fila_num}: Fecha de garantía inválida '{garantia_val}'")
            
            # Crear objeto de datos para el equipo
            equipo_data = {
                'nombre': nombre,
                'tipo': tipo,
                'area': area,
                'estado': estado,
                'marca': marca,
                'modelo': modelo,
                'precio': precio,
                'proveedor': proveedor,
                'observacion': observacion,
                'fecha_compra': fecha_compra,
                'garantia_hasta': garantia_hasta,
                'fila': fila_num
            }
            
            equipos_procesados.append(equipo_data)
            
        except Exception as e:
            errores.append(f"Fila {fila_num}: Error procesando datos - {str(e)}")
    
    return True, equipos_procesados, errores

def crear_equipos_masivo(equipos_data):
    """
    Crea los equipos en la base de datos de forma masiva
    """
    equipos_creados = []
    errores = []
    
    for equipo_data in equipos_data:
        try:
            fila = equipo_data.pop('fila')
            
            # Verificar si ya existe un equipo con el mismo nombre en la misma área
            if Equipo.objects.filter(
                nombre__iexact=equipo_data['nombre'], 
                area=equipo_data['area']
            ).exists():
                errores.append(f"Fila {fila}: Ya existe un equipo '{equipo_data['nombre']}' en el área '{equipo_data['area'].nombre}'")
                continue
            
            # Crear el equipo
            equipo = Equipo.objects.create(**equipo_data)
            equipos_creados.append(equipo)
            
        except Exception as e:
            errores.append(f"Fila {fila}: Error al crear equipo - {str(e)}")
    
    return equipos_creados, errores

def generar_plantilla_excel():
    """
    Genera un archivo Excel de plantilla para importación
    """
    # Datos de ejemplo
    data = {
        'Nombre': [
            'Compresor Industrial A1',
            'Motor Eléctrico B2',
            'Bomba Centrífuga C3'
        ],
        'Tipo': [
            'Compresor',
            'Motor',
            'Bomba'
        ],
        'Area': [
            'Producción',
            'Mantenimiento',
            'Utilidades'
        ],
        'Estado': [
            'Operativo',
            'En Mantenimiento',
            'Operativo'
        ],
        'Marca': [
            'Atlas Copco',
            'WEG',
            'Grundfos'
        ],
        'Modelo': [
            'GA37VSD',
            'W22-132S',
            'CR15-04'
        ],
        'Precio': [
            15000.00,
            2500.50,
            1800.75
        ],
        'Proveedor': [
            'Equipos Industriales S.A.',
            'Motores y Más Ltda.',
            'Bombas del Norte'
        ],
        'Observacion': [
            'Compresor de alta eficiencia con variador de frecuencia',
            'Motor trifásico para uso industrial',
            'Bomba centrífuga multietapa'
        ],
        'Fecha_Compra': [
            '2023-01-15',
            '2023-02-20',
            '2023-03-10'
        ],
        'Garantia_Hasta': [
            '2025-01-15',
            '2024-02-20',
            '2024-03-10'
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Crear archivo en memoria
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Equipos', index=False)
        
        # Obtener el workbook y la hoja
        workbook = writer.book
        worksheet = writer.sheets['Equipos']
        
        # Ajustar ancho de columnas
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    buffer.seek(0)
    return buffer 