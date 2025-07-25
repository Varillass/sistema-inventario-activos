#!/usr/bin/env python3
"""
Script para insertar datos iniciales en la base de datos MySQL
"""

import pymysql
from datetime import date

# Configuración de conexión
DB_CONFIG = {
    'host': '181.224.226.142',
    'user': 'afrodita',
    'password': 'Zxasqw12@@@',
    'database': 'inventario_activos',
    'port': 3306
}

def insert_areas(cursor):
    """Insertar áreas iniciales"""
    areas = [
        ('Administración', 'Área administrativa y de gestión'),
        ('Producción', 'Área de producción y manufactura'),
        ('Mantenimiento', 'Área de mantenimiento y reparaciones'),
        ('Almacén', 'Área de almacenamiento y logística'),
        ('IT/Tecnología', 'Área de tecnologías de la información'),
        ('Recursos Humanos', 'Área de recursos humanos'),
        ('Contabilidad', 'Área de contabilidad y finanzas'),
        ('Ventas', 'Área de ventas y comercialización'),
        ('Marketing', 'Área de marketing y publicidad'),
        ('Seguridad', 'Área de seguridad y vigilancia')
    ]
    
    for area in areas:
        cursor.execute(
            "INSERT INTO inventario_area (nombre, descripcion) VALUES (%s, %s)",
            area
        )
    print("✅ Áreas insertadas exitosamente")

def insert_estados(cursor):
    """Insertar estados iniciales"""
    estados = [
        ('Operativo', 'Equipo funcionando correctamente'),
        ('Inoperativo', 'Equipo fuera de servicio'),
        ('En Mantenimiento', 'Equipo en proceso de mantenimiento'),
        ('En Reparación', 'Equipo siendo reparado'),
        ('Fuera de Servicio', 'Equipo retirado del servicio'),
        ('En Almacén', 'Equipo almacenado temporalmente')
    ]
    
    for estado in estados:
        cursor.execute(
            "INSERT INTO inventario_estado (nombre, descripcion) VALUES (%s, %s)",
            estado
        )
    print("✅ Estados insertados exitosamente")

def insert_equipos_prueba(cursor):
    """Insertar equipos de prueba"""
    equipos = [
        ('Computadora Administrativa', 'Computadora', 'Com-00001', 'Dell', 'OptiPlex 7090', 1200.00, 'Dell Technologies', '2023-01-15', '2026-01-15', 'Equipo principal para gestión administrativa', 1, 1, '2024-01-15'),
        ('Impresora Multifuncional', 'Impresora', 'Imp-00001', 'HP', 'LaserJet Pro M404n', 450.00, 'HP Inc.', '2023-02-20', '2025-02-20', 'Impresora para área administrativa', 1, 1, '2024-01-15'),
        ('Servidor Web', 'Servidor', 'Ser-00001', 'Dell', 'PowerEdge R740', 3500.00, 'Dell Technologies', '2023-03-10', '2028-03-10', 'Servidor principal para aplicaciones web', 5, 1, '2024-01-15'),
        ('Switch de Red', 'Red', 'Red-00001', 'Cisco', 'Catalyst 2960', 800.00, 'Cisco Systems', '2023-04-05', '2026-04-05', 'Switch para red local', 5, 1, '2024-01-15'),
        ('Compresor Industrial', 'Compresor', 'Com-00002', 'Ingersoll Rand', 'SSR-EP-75', 2500.00, 'Ingersoll Rand', '2023-05-12', '2025-05-12', 'Compresor para área de producción', 2, 1, '2024-01-15'),
        ('Máquina CNC', 'Maquinaria', 'Maq-00001', 'Haas', 'VF-2', 45000.00, 'Haas Automation', '2023-06-18', '2028-06-18', 'Máquina CNC para fabricación', 2, 1, '2024-01-15'),
        ('Cámara de Seguridad', 'Seguridad', 'Seg-00001', 'Hikvision', 'DS-2CD2142FWD-I', 150.00, 'Hikvision', '2023-07-22', '2025-07-22', 'Cámara para vigilancia exterior', 10, 1, '2024-01-15'),
        ('Aire Acondicionado', 'Climatización', 'Cli-00001', 'LG', 'Multi V IV', 1800.00, 'LG Electronics', '2023-08-30', '2026-08-30', 'Sistema de aire acondicionado central', 1, 1, '2024-01-15'),
        ('Escáner de Códigos', 'Escáner', 'Esc-00001', 'Honeywell', '1900GHD', 200.00, 'Honeywell', '2023-09-14', '2025-09-14', 'Escáner para inventario', 4, 1, '2024-01-15'),
        ('Proyector Multimedia', 'Proyector', 'Pro-00001', 'Epson', 'PowerLite 118', 600.00, 'Epson', '2023-10-08', '2026-10-08', 'Proyector para presentaciones', 1, 1, '2024-01-15')
    ]
    
    for equipo in equipos:
        cursor.execute("""
            INSERT INTO inventario_equipo 
            (nombre, tipo, numero_serie, marca, modelo, precio, proveedor, fecha_compra, garantia_hasta, observacion, fecha_registro, area_id, estado_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, equipo)
    
    print("✅ Equipos de prueba insertados exitosamente")

def main():
    """Función principal"""
    try:
        # Conectar a la base de datos
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("🔄 Conectando a la base de datos...")
        
        # Insertar datos iniciales
        insert_areas(cursor)
        insert_estados(cursor)
        insert_equipos_prueba(cursor)
        
        # Confirmar cambios
        conn.commit()
        print("✅ Todos los datos se insertaron correctamente")
        
        # Mostrar estadísticas
        cursor.execute("SELECT COUNT(*) FROM inventario_area")
        areas_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM inventario_estado")
        estados_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM inventario_equipo")
        equipos_count = cursor.fetchone()[0]
        
        print(f"\n📊 Estadísticas:")
        print(f"   - Áreas: {areas_count}")
        print(f"   - Estados: {estados_count}")
        print(f"   - Equipos: {equipos_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main() 