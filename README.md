# ABPfinalSkyeRoute
un nuevo repositorio con la entrega final del ABP
Menu con las funciones requeridas en las evidencias

Grupo: 37 JESUS MARIA

Participantes:
Arruti Osses Julian Alejandro
DNI: 40679156
julianarruti006@gmail.com

Farid Yusef Mrad Caro
DNI: 36126623
ishary321@gmail.com

Arruti Osses Marcos Agustin
DNI: 36725634
marcosartificialintelligence@gmail.com

Breve descripcion del proyecto:
esta modularizado en clientes, destinos, y ventas, todos esos modulos los llama desde el main
Despues tenes el gitignore que es para que no cargue todas las librerias al github
y el requirements.txt para que se instalen las librerias necesarias para correr el programa en este caso usamos MySQL 9.3 y MySQL workbench 8.0 y el unico requisito es mysqlconnector

Los profesores deberan crear una base de datos con el script que se encuentra en la carpeta base de datos y conectarla con Main.py si desean comprobar todas las funcionalidades.




Por las dudas dejo el script aca tambien:
-- SQL Script para la creación de la base de datos y tablas de SkyeRoute_DB
-- Diseñado para ser ejecutado en MySQL Workbench o línea de comandos.

-- 1. Crear la base de datos
CREATE DATABASE IF NOT EXISTS skyeroute_ARRUTI;

-- 2. Usar la base de datos recién creada (o ya existente)
USE skyeroute_ARRUTI;

-- 3. Desactivar temporalmente la verificación de claves foráneas
-- Esto es útil para evitar errores de orden al crear tablas con FKs o insertar datos.
SET FOREIGN_KEY_CHECKS = 0;

-- 4. Creación de la tabla 'clientes'
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    razon_social VARCHAR(100) NOT NULL,
    cuit VARCHAR(15) UNIQUE NOT NULL, -- CUIT debe ser único
    correo_electronico VARCHAR(100) UNIQUE NOT NULL -- Correo debe ser único
);

-- 6. Creación de la tabla 'destinos'
CREATE TABLE destinos (
    id_destino INT AUTO_INCREMENT PRIMARY KEY,
    ciudad VARCHAR(100) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    costo_base DECIMAL(10, 2) NOT NULL
);

-- 7. Creación de la tabla 'ventas'
CREATE TABLE ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_destino INT NOT NULL,
    fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora de la venta, por defecto la actual
    costo_venta DECIMAL(10, 2) NOT NULL,
    estado_venta ENUM('Activa', 'Anulada') DEFAULT 'Activa', -- Estado de la venta
    fecha_anulacion DATETIME NULL, -- Fecha y hora de anulación, nulo si no está anulada
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_destino) REFERENCES destinos(id_destino)
);

-- 8. Reactivar la verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;

-- 9. Inserción de datos de prueba iniciales

-- Clientes de prueba (5 antiguos, 5 recientes para probar el botón de arrepentimiento)
INSERT INTO clientes (razon_social, cuit, correo_electronico) VALUES
('Antigua Data S.A.', '30-11111111-1', 'antigua1@mail.com'),
('Cliente Viejo SRL', '20-22222222-2', 'viejo2@mail.com'),
('Historico Viajes', '27-33333333-3', 'historico3@mail.com'),
('Decadas de Aventura', '30-44444444-4', 'decadas4@mail.com'),
('Pasado Glorioso S.A.', '20-55555555-5', 'pasado5@mail.com'),
('Nuevo Cliente S.A.', '30-66666666-6', 'nuevo1@mail.com'),
('Fresca Empresa SRL', '20-77777777-7', 'fresca2@mail.com'),
('Hoy Mismo Viajes', '27-88888888-8', 'hoymismo3@mail.com'),
('Actual Aventuras', '30-99999999-9', 'actual4@mail.com'),
('Presente Tours', '20-00000000-0', 'presente5@mail.com');

-- Destinos de prueba
INSERT INTO destinos (ciudad, pais, costo_base) VALUES
('París', 'Francia', 850.00),
('Tokio', 'Japón', 1200.00),
('Nueva York', 'USA', 950.00),
('Roma', 'Italia', 700.00),
('Sidney', 'Australia', 1500.00);


INSERT INTO ventas (id_cliente, id_destino, fecha_venta, costo_venta, estado_venta) VALUES
((SELECT id_cliente FROM clientes WHERE razon_social = 'Antigua Data S.A.'), (SELECT id_destino FROM destinos WHERE ciudad = 'París'), '2025-03-01 10:00:00', 850.00, 'Activa'),
((SELECT id_cliente FROM clientes WHERE razon_social = 'Nuevo Cliente S.A.'), (SELECT id_destino FROM destinos WHERE ciudad = 'Tokio'), NOW(), 1200.00, 'Activa');

------------------------------
hasta aca el script de la base de datos.
-------------------------------


CONSULTAS SUGERIDAS Y EXPLICADAS:
Consulta 1: Listar todos los Clientes, incluyendo los antiguos y recientes.

USE skyeroute_arruti;

SELECT
    id_cliente,
    razon_social,
    cuit,
    correo_electronico
FROM
    clientes
ORDER BY
    id_cliente;

Consulta 2: Mostrar todas las Ventas, con la información del Cliente y el Destino.

Esta consulta te permite ver todas las ventas registradas, incluyendo si están activas o anuladas, y los detalles del cliente y destino asociados.

SELECT
    v.id_venta,
    c.razon_social AS NombreCliente,
    d.ciudad AS CiudadDestino,
    d.pais AS PaisDestino,
    v.fecha_venta,
    v.costo_venta,
    v.estado_venta,
    v.fecha_anulacion
FROM
    ventas v
JOIN
    clientes c ON v.id_cliente = c.id_cliente
JOIN
    destinos d ON v.id_destino = d.id_destino
ORDER BY
    v.fecha_venta DESC;

Consulta 3: Obtener la última Venta registrada por cada Cliente.

Esta consulta es útil para ver la actividad más reciente de cada cliente que ha realizado una venta.

SELECT
    c.razon_social AS Cliente,
    MAX(v.fecha_venta) AS UltimaFechaVenta,
    MAX(v.costo_venta) AS CostoUltimaVenta -- Podría ser el costo de la última venta, no necesariamente el MAX
FROM
    ventas v
JOIN
    clientes c ON v.id_cliente = c.id_cliente
GROUP BY
    c.razon_social
ORDER BY
    UltimaFechaVenta DESC;

¡Perfecto! El script SQL actualizado con tu nombre en la base de datos (skyeroute_ARRUTI) y la eliminación de las sentencias DROP TABLE explícitas (aunque se podrían añadir si se desea una "limpieza total" antes de la recreación) está excelente.

Ahora, para que el profesor pueda probar y ver el funcionamiento de la base de datos directamente en MySQL Workbench, aquí tienes 5 consultas SQL. Estas consultas están diseñadas para mostrar la interacción con los datos que has insertado y verificar la estructura de la base de datos, además de algunas capacidades de análisis.

Consultas SQL para el Profesor (para ejecutar en MySQL Workbench)
Estas consultas están pensadas para que el profesor las ejecute directamente en MySQL Workbench después de haber corrido tu script skyeroute_db_setup.sql.

Consulta 1: Listar todos los Clientes, incluyendo los antiguos y recientes.

SQL

-- Consulta 1: Listar todos los clientes registrados
USE skyeroute_ARRUTI;

SELECT
    id_cliente,
    razon_social,
    cuit,
    correo_electronico
FROM
    clientes
ORDER BY
    id_cliente;
Consulta 2: Mostrar todas las Ventas, con la información del Cliente y el Destino.

Esta consulta te permite ver todas las ventas registradas, incluyendo si están activas o anuladas, y los detalles del cliente y destino asociados.

SQL

-- Consulta 2: Mostrar todas las ventas con detalles de cliente y destino
USE skyeroute_ARRUTI;

SELECT
    v.id_venta,
    c.razon_social AS NombreCliente,
    d.ciudad AS CiudadDestino,
    d.pais AS PaisDestino,
    v.fecha_venta,
    v.costo_venta,
    v.estado_venta,
    v.fecha_anulacion
FROM
    ventas v
JOIN
    clientes c ON v.id_cliente = c.id_cliente
JOIN
    destinos d ON v.id_destino = d.id_destino
ORDER BY
    v.fecha_venta DESC;
Consulta 3: Obtener la última Venta registrada por cada Cliente.

Esta consulta es útil para ver la actividad más reciente de cada cliente que ha realizado una venta.

SQL

-- Consulta 3: Obtener la última venta de cada cliente y su fecha
USE skyeroute_ARRUTI;

SELECT
    c.razon_social AS Cliente,
    MAX(v.fecha_venta) AS UltimaFechaVenta,
    MAX(v.costo_venta) AS CostoUltimaVenta -- Podría ser el costo de la última venta, no necesariamente el MAX
FROM
    ventas v
JOIN
    clientes c ON v.id_cliente = c.id_cliente
GROUP BY
    c.razon_social
ORDER BY
    UltimaFechaVenta DESC;

Consulta 4: Listar todos los Destinos cuyo nombre de Ciudad o País empieza con una letra específica.

--con 'N' (ejemplo)

USE skyeroute_ARRUTI;

SELECT
    id_destino,
    ciudad,
    pais,
    costo_base
FROM
    destinos
WHERE
    ciudad LIKE 'N%' OR pais LIKE 'N%' -- Cambiar 'N%' por la letra que se desee probar
ORDER BY
    ciudad;

Consulta 5: Mostrar cuántas Ventas se realizaron por País de destino y el Total de ingresos por cada uno.


SELECT
    d.pais AS PaisDestino,
    COUNT(v.id_venta) AS NumeroDeVentas,
    SUM(v.costo_venta) AS TotalIngresos
FROM
    ventas v
JOIN
    destinos d ON v.id_destino = d.id_destino
GROUP BY
    d.pais
ORDER BY
    TotalIngresos DESC;