#!/usr/bin/env bash
set -o errexit

echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --no-input

echo "Intentando conectar a MySQL..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_activos.settings')
django.setup()

from django.db import connection
try:
    connection.ensure_connection()
    print('✅ Conexión a MySQL exitosa')
    mysql_available = True
except Exception as e:
    print('⚠️ Error conectando a MySQL:', str(e))
    print('🔄 Cambiando a SQLite...')
    mysql_available = False
"

if [ $? -ne 0 ]; then
    echo "🔄 Configurando para usar SQLite..."
    export DJANGO_SETTINGS_MODULE=inventario_activos.settings_sqlite_fallback
fi

echo "Ejecutando migraciones..."
python manage.py migrate

echo "Configurando datos iniciales..."
python -c "
from django.core.management import execute_from_command_line
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_activos.settings')
django.setup()

from django.contrib.auth import get_user_model
from inventario.models import Area, Estado

# Crear superusuario
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@inventario.com', 'admin123')
    print('Superusuario creado: admin/admin123')

# Crear usuarios adicionales
usuarios_adicionales = [
    {'username': 'inventario', 'email': 'inventario@empresa.com', 'password': 'inventario123', 'first_name': 'Usuario', 'last_name': 'Inventario'},
    {'username': 'supervisor', 'email': 'supervisor@empresa.com', 'password': 'supervisor123', 'first_name': 'Usuario', 'last_name': 'Supervisor'},
]

for user_data in usuarios_adicionales:
    if not User.objects.filter(username=user_data['username']).exists():
        User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        print('Usuario creado: ' + user_data['username'] + '/' + user_data['password'])

# Crear áreas
areas = ['Administración', 'Contabilidad', 'Ventas', 'Almacén', 'Sistemas', 'Recursos Humanos', 'Mantenimiento']
for nombre in areas:
    Area.objects.get_or_create(nombre=nombre)

# Crear estados  
estados = ['Nuevo', 'Bueno', 'Regular', 'Malo', 'En Reparación', 'Dado de Baja']
for nombre in estados:
    Estado.objects.get_or_create(nombre=nombre)

print('Configuración completada')
"

echo "Build completado exitosamente!" 