-- Script para insertar datos de prueba en el sistema de inventario
-- Ejecutar después de create_tables_mysql.sql

USE inventario_activos;

-- Insertar equipos de prueba
INSERT INTO inventario_equipo (nombre, tipo, numero_serie, marca, modelo, precio, proveedor, fecha_compra, garantia_hasta, observacion, fecha_registro, area_id, estado_id) VALUES
('Computadora Administrativa', 'Computadora', 'Com-00001', 'Dell', 'OptiPlex 7090', 1200.00, 'Dell Technologies', '2023-01-15', '2026-01-15', 'Equipo principal para gestión administrativa', '2023-01-15', 1, 1),
('Impresora Multifuncional', 'Impresora', 'Imp-00001', 'HP', 'LaserJet Pro M404n', 450.00, 'HP Inc.', '2023-02-20', '2025-02-20', 'Impresora para área administrativa', '2023-02-20', 1, 1),
('Servidor Web', 'Servidor', 'Ser-00001', 'Dell', 'PowerEdge R740', 3500.00, 'Dell Technologies', '2023-03-10', '2028-03-10', 'Servidor principal para aplicaciones web', '2023-03-10', 5, 1),
('Switch de Red', 'Red', 'Red-00001', 'Cisco', 'Catalyst 2960', 800.00, 'Cisco Systems', '2023-04-05', '2026-04-05', 'Switch para red local', '2023-04-05', 5, 1),
('Compresor Industrial', 'Compresor', 'Com-00002', 'Ingersoll Rand', 'SSR-EP-75', 2500.00, 'Ingersoll Rand', '2023-05-12', '2025-05-12', 'Compresor para área de producción', '2023-05-12', 2, 1),
('Máquina CNC', 'Maquinaria', 'Maq-00001', 'Haas', 'VF-2', 45000.00, 'Haas Automation', '2023-06-18', '2028-06-18', 'Máquina CNC para fabricación', '2023-06-18', 2, 1),
('Cámara de Seguridad', 'Seguridad', 'Seg-00001', 'Hikvision', 'DS-2CD2142FWD-I', 150.00, 'Hikvision', '2023-07-22', '2025-07-22', 'Cámara para vigilancia exterior', '2023-07-22', 10, 1),
('Aire Acondicionado', 'Climatización', 'Cli-00001', 'LG', 'Multi V IV', 1800.00, 'LG Electronics', '2023-08-30', '2026-08-30', 'Sistema de aire acondicionado central', '2023-08-30', 1, 1),
('Escáner de Códigos', 'Escáner', 'Esc-00001', 'Honeywell', '1900GHD', 200.00, 'Honeywell', '2023-09-14', '2025-09-14', 'Escáner para inventario', '2023-09-14', 4, 1),
('Proyector Multimedia', 'Proyector', 'Pro-00001', 'Epson', 'PowerLite 118', 600.00, 'Epson', '2023-10-08', '2026-10-08', 'Proyector para presentaciones', '2023-10-08', 1, 1),
('Equipo en Mantenimiento', 'Computadora', 'Com-00003', 'Lenovo', 'ThinkCentre M90', 900.00, 'Lenovo', '2023-11-05', '2026-11-05', 'Equipo en proceso de actualización', '2023-11-05', 5, 3),
('Equipo Fuera de Servicio', 'Impresora', 'Imp-00002', 'Canon', 'Pixma TS8320', 300.00, 'Canon', '2022-12-10', '2024-12-10', 'Equipo retirado por obsolescencia', '2022-12-10', 1, 5),
('Router WiFi', 'Red', 'Red-00002', 'TP-Link', 'Archer C7', 80.00, 'TP-Link', '2023-01-20', '2025-01-20', 'Router para red WiFi', '2023-01-20', 5, 1),
('Monitor LED', 'Monitor', 'Mon-00001', 'Samsung', 'LS24F350FHL', 180.00, 'Samsung', '2023-02-28', '2026-02-28', 'Monitor para estación de trabajo', '2023-02-28', 5, 1),
('Teclado Inalámbrico', 'Periférico', 'Per-00001', 'Logitech', 'K780', 60.00, 'Logitech', '2023-03-15', '2025-03-15', 'Teclado inalámbrico ergonómico', '2023-03-15', 5, 1);

-- Mostrar estadísticas
SELECT 
    'Estadísticas del Inventario' as titulo,
    COUNT(*) as total_equipos,
    COUNT(CASE WHEN estado_id = 1 THEN 1 END) as operativos,
    COUNT(CASE WHEN estado_id = 2 THEN 1 END) as inoperativos,
    COUNT(CASE WHEN estado_id = 3 THEN 1 END) as en_mantenimiento,
    COUNT(CASE WHEN estado_id = 5 THEN 1 END) as fuera_servicio
FROM inventario_equipo;

-- Mostrar equipos por área
SELECT 
    a.nombre as area,
    COUNT(e.id) as cantidad_equipos
FROM inventario_area a
LEFT JOIN inventario_equipo e ON a.id = e.area_id
GROUP BY a.id, a.nombre
ORDER BY cantidad_equipos DESC;

-- Mostrar equipos por tipo
SELECT 
    tipo,
    COUNT(*) as cantidad
FROM inventario_equipo
GROUP BY tipo
ORDER BY cantidad DESC; 