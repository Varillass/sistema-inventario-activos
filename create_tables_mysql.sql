-- Script SQL para crear las tablas del sistema de inventario de activos
-- Ejecutar en MySQL: mysql -u afrodita -p inventario_activos < create_tables_mysql.sql

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS inventario_activos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE inventario_activos;

-- Tabla de áreas
CREATE TABLE IF NOT EXISTS inventario_area (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT NOT NULL
);

-- Tabla de estados
CREATE TABLE IF NOT EXISTS inventario_estado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT NOT NULL
);

-- Tabla de equipos
CREATE TABLE IF NOT EXISTS inventario_equipo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    numero_serie VARCHAR(50) UNIQUE,
    marca VARCHAR(100),
    modelo VARCHAR(100),
    precio DECIMAL(10,2),
    proveedor VARCHAR(100),
    fecha_compra DATE,
    garantia_hasta DATE,
    observacion TEXT,
    fecha_registro DATE NOT NULL,
    area_id INT NOT NULL,
    estado_id INT NOT NULL,
    FOREIGN KEY (area_id) REFERENCES inventario_area(id),
    FOREIGN KEY (estado_id) REFERENCES inventario_estado(id)
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX idx_equipo_area ON inventario_equipo(area_id);
CREATE INDEX idx_equipo_estado ON inventario_equipo(estado_id);
CREATE INDEX idx_equipo_tipo ON inventario_equipo(tipo);
CREATE INDEX idx_equipo_fecha_registro ON inventario_equipo(fecha_registro);

-- Insertar datos iniciales de áreas
INSERT INTO inventario_area (nombre, descripcion) VALUES
('Administración', 'Área administrativa y de gestión'),
('Producción', 'Área de producción y manufactura'),
('Mantenimiento', 'Área de mantenimiento y reparaciones'),
('Almacén', 'Área de almacenamiento y logística'),
('IT/Tecnología', 'Área de tecnologías de la información'),
('Recursos Humanos', 'Área de recursos humanos'),
('Contabilidad', 'Área de contabilidad y finanzas'),
('Ventas', 'Área de ventas y comercialización'),
('Marketing', 'Área de marketing y publicidad'),
('Seguridad', 'Área de seguridad y vigilancia');

-- Insertar datos iniciales de estados
INSERT INTO inventario_estado (nombre, descripcion) VALUES
('Operativo', 'Equipo funcionando correctamente'),
('Inoperativo', 'Equipo fuera de servicio'),
('En Mantenimiento', 'Equipo en proceso de mantenimiento'),
('En Reparación', 'Equipo siendo reparado'),
('Fuera de Servicio', 'Equipo retirado del servicio'),
('En Almacén', 'Equipo almacenado temporalmente');

-- Crear usuario para la aplicación si no existe
-- CREATE USER IF NOT EXISTS 'afrodita'@'%' IDENTIFIED BY 'zxasqw12@@@';
-- GRANT ALL PRIVILEGES ON inventario_activos.* TO 'afrodita'@'%';
-- FLUSH PRIVILEGES;

-- Mostrar las tablas creadas
SHOW TABLES;

-- Mostrar estructura de las tablas principales
DESCRIBE inventario_area;
DESCRIBE inventario_estado;
DESCRIBE inventario_equipo; 