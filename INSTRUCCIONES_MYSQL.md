# Instrucciones para Configurar MySQL y Crear las Tablas

## 1. Conectar a tu servidor MySQL

Desde tu servidor MySQL, ejecuta:

```bash
mysql -u root -p
```

## 2. Crear la base de datos y usuario

```sql
-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS inventario_activos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario para la aplicación
CREATE USER IF NOT EXISTS 'afrodita'@'%' IDENTIFIED BY 'zxasqw12@@@';

-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON inventario_activos.* TO 'afrodita'@'%';

-- Aplicar cambios
FLUSH PRIVILEGES;

-- Seleccionar la base de datos
USE inventario_activos;
```

## 3. Ejecutar el script de creación de tablas

Desde tu servidor MySQL, ejecuta:

```bash
mysql -u afrodita -p inventario_activos < create_tables_mysql.sql
```

O copia y pega el contenido del archivo `create_tables_mysql.sql` directamente en el cliente MySQL.

## 4. Insertar datos de prueba (opcional)

```bash
mysql -u afrodita -p inventario_activos < insert_test_data.sql
```

## 5. Verificar que todo funciona

```sql
-- Ver las tablas creadas
SHOW TABLES;

-- Ver la estructura de la tabla principal
DESCRIBE inventario_equipo;

-- Ver datos de prueba
SELECT * FROM inventario_equipo LIMIT 5;
```

## 6. Configurar MySQL para conexiones remotas

Si necesitas que Django se conecte desde tu máquina local:

### Editar configuración MySQL:
```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

Cambiar:
```ini
bind-address = 127.0.0.1
```

Por:
```ini
bind-address = 0.0.0.0
```

### Reiniciar MySQL:
```bash
sudo systemctl restart mysql
```

### Abrir puerto en firewall:
```bash
sudo ufw allow 3306
```

## 7. Probar conexión desde tu máquina local

```bash
mysql -h 181.224.226.142 -u afrodita -p inventario_activos
```

## 8. Ejecutar migraciones de Django

Una vez que la conexión funcione, ejecuta:

```bash
python manage.py migrate
```

## Estructura de las Tablas

### inventario_area
- `id`: Identificador único
- `nombre`: Nombre del área (único)
- `descripcion`: Descripción del área

### inventario_estado
- `id`: Identificador único
- `nombre`: Nombre del estado (único)
- `descripcion`: Descripción del estado

### inventario_equipo
- `id`: Identificador único
- `nombre`: Nombre del equipo
- `tipo`: Tipo de equipo
- `numero_serie`: Número de serie (único)
- `marca`: Marca del equipo
- `modelo`: Modelo del equipo
- `precio`: Precio del equipo
- `proveedor`: Proveedor del equipo
- `fecha_compra`: Fecha de compra
- `garantia_hasta`: Fecha de vencimiento de garantía
- `observacion`: Observaciones del equipo
- `fecha_registro`: Fecha de registro en el sistema
- `area_id`: Referencia al área (clave foránea)
- `estado_id`: Referencia al estado (clave foránea)

## Datos Iniciales

El script incluye:
- 10 áreas predefinidas (Administración, Producción, etc.)
- 6 estados predefinidos (Operativo, Inoperativo, etc.)
- 15 equipos de prueba con datos realistas 