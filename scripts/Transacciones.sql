-- Crear tabla de dimensión DimTiempo
CREATE TABLE DimTiempo (
    id_tiempo SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    dia_semana VARCHAR(20),
    mes VARCHAR(20),
    trimestre INT,
    anio INT
);

-- Crear tabla de dimensión DimProducto
CREATE TABLE DimProducto (
    id_producto SERIAL PRIMARY KEY,
    nombre_producto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    precio DECIMAL(10, 2),
    proveedor VARCHAR(100)
);

-- Crear tabla de dimensión DimCliente
CREATE TABLE DimCliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre_cliente VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(20),
    email VARCHAR(100)
);

-- Crear tabla de dimensión DimEmpleado
CREATE TABLE DimEmpleado (
    id_empleado SERIAL PRIMARY KEY,
    nombre_empleado VARCHAR(100) NOT NULL,
    puesto VARCHAR(50),
    fecha_contratacion DATE
);

-- Crear tabla de dimensión DimTienda
CREATE TABLE DimTienda (
    id_tienda SERIAL PRIMARY KEY,
    nombre_tienda VARCHAR(100) NOT NULL,
    direccion_tienda VARCHAR(200),
    ciudad VARCHAR(100),
    pais VARCHAR(100)
);

-- Crear tabla de hechos HechosVentas
CREATE TABLE HechosVentas (
    id_venta SERIAL PRIMARY KEY,
    id_tiempo INT NOT NULL,
    id_producto INT NOT NULL,
    id_cliente INT NOT NULL,
    id_empleado INT NOT NULL,
    id_tienda INT NOT NULL,
    cantidad INT NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    costo_total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_tiempo) REFERENCES DimTiempo(id_tiempo),
    FOREIGN KEY (id_producto) REFERENCES DimProducto(id_producto),
    FOREIGN KEY (id_cliente) REFERENCES DimCliente(id_cliente),
    FOREIGN KEY (id_empleado) REFERENCES DimEmpleado(id_empleado),
    FOREIGN KEY (id_tienda) REFERENCES DimTienda(id_tienda)
);

-- Insertar datos en DimTiempo
INSERT INTO DimTiempo (fecha, dia_semana, mes, trimestre, anio) VALUES
('2024-07-01', 'Lunes', 'Julio', 3, 2024),
('2024-07-02', 'Martes', 'Julio', 3, 2024),
('2024-07-03', 'Miércoles', 'Julio', 3, 2024),
('2024-07-04', 'Jueves', 'Julio', 3, 2024),
('2024-07-05', 'Viernes', 'Julio', 3, 2024);

-- Insertar datos en DimProducto
INSERT INTO DimProducto (nombre_producto, categoria, precio, proveedor) VALUES
('Tarta de Manzana', 'Tartas', 10.00, 'ProveedorA'),
('Brownie', 'Pasteles', 8.00, 'ProveedorB'),
('Cupcake', 'Pasteles', 5.00, 'ProveedorC'),
('Panque de Limón', 'Pasteles', 7.00, 'ProveedorD'),
('Croissant', 'Pan', 3.00, 'ProveedorE');

-- Insertar datos en DimCliente
INSERT INTO DimCliente (nombre_cliente, direccion, telefono, email) VALUES
('Juan Pérez', 'Calle 123, Ciudad', '555-1234', 'juan@mail.com'),
('María López', 'Av. 45, Ciudad', '555-5678', 'maria@mail.com'),
('Carlos Sánchez', 'Boulevard 678, Ciudad', '555-8765', 'carlos@mail.com'),
('Ana Ramírez', 'Plaza 12, Ciudad', '555-4321', 'ana@mail.com'),
('Luis Fernández', 'Pasaje 9, Ciudad', '555-6789', 'luis@mail.com');

-- Insertar datos en DimEmpleado
INSERT INTO DimEmpleado (nombre_empleado, puesto, fecha_contratacion) VALUES
('Carlos Gómez', 'Vendedor', '2020-01-15'),
('Ana Ruiz', 'Cajero', '2019-06-10'),
('Luis Martínez', 'Gerente', '2018-03-20'),
('Sofía Torres', 'Vendedor', '2021-09-01'),
('Pedro Castillo', 'Cajero', '2019-11-30');

-- Insertar datos en DimTienda
INSERT INTO DimTienda (nombre_tienda, direccion_tienda, ciudad, pais) VALUES
('Pastelería A', 'Calle 456, Ciudad A', 'Ciudad A', 'País A'),
('Pastelería B', 'Av. 78, Ciudad B', 'Ciudad B', 'País B'),
('Pastelería C', 'Boulevard 90, Ciudad C', 'Ciudad C', 'País C'),
('Pastelería D', 'Plaza 23, Ciudad D', 'Ciudad D', 'País D'),
('Pastelería E', 'Pasaje 11, Ciudad E', 'Ciudad E', 'País E');

-- Insertar datos en HechosVentas
INSERT INTO HechosVentas (id_tiempo, id_producto, id_cliente, id_empleado, id_tienda, cantidad, monto, costo_total) VALUES
(1, 1, 1, 1, 1, 2, 20.00, 15.00),
(1, 2, 2, 2, 2, 1, 8.00, 6.00),
(2, 3, 3, 3, 3, 3, 15.00, 10.00),
(2, 4, 4, 4, 4, 1, 7.00, 5.00),
(3, 5, 5, 5, 5, 4, 12.00, 9.00),
(3, 1, 1, 1, 1, 2, 20.00, 15.00),
(4, 2, 2, 2, 2, 1, 8.00, 6.00),
(4, 3, 3, 3, 3, 3, 15.00, 10.00),
(5, 4, 4, 4, 4, 1, 7.00, 5.00),
(5, 5, 5, 5, 5, 4, 12.00, 9.00);
