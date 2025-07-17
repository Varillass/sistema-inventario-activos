#!/usr/bin/env bash
# exit on error
set -o errexit

# Actualizar pip y instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Verificar que psycopg2 esté instalado correctamente
pip show psycopg2-binary

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario si no existe (usando variables de entorno)
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@inventario.com', 'admin123')
    print('Superusuario creado: admin/admin123')
else:
    print('Superusuario ya existe')
EOF

# Crear datos iniciales
python manage.py shell <<EOF
from inventario.models import Area, Estado

# Crear áreas si no existen
areas_iniciales = [
    'Administración', 'Contabilidad', 'Ventas', 'Almacén', 
    'Sistemas', 'Recursos Humanos', 'Mantenimiento'
]

for nombre_area in areas_iniciales:
    area, created = Area.objects.get_or_create(nombre=nombre_area)
    if created:
        print(f'Área creada: {nombre_area}')

# Crear estados si no existen
estados_iniciales = [
    'Nuevo', 'Bueno', 'Regular', 'Malo', 
    'En Reparación', 'Dado de Baja'
]

for nombre_estado in estados_iniciales:
    estado, created = Estado.objects.get_or_create(nombre=nombre_estado)
    if created:
        print(f'Estado creado: {nombre_estado}')

print('Datos iniciales configurados correctamente')
EOF 