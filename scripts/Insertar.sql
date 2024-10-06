-- Insertar datos en la tabla 'pasteleria'
INSERT INTO pasteleria (id, nombre, email, telefono, direccion, ciudad, codigo_postal, url_website, fecha_registro)
VALUES 
('123e4567-e89b-12d3-a456-426614174000', 'Pastelería Dulce Sabor', 'contacto@dulcesabor.com', '555-1234', 'Calle 123', 'Ciudad Pastel', '12345', 'www.dulcesabor.com', '2023-01-15'),
('223e4567-e89b-12d3-a456-426614174001', 'La Repostera', 'info@larepostera.com', '555-5678', 'Avenida de los Postres 456', 'Ciudad Pastel', '67890', 'www.larepostera.com', '2023-03-22');

-- Insertar datos en la tabla 'rol'
INSERT INTO rol (id_pasteleria, nombre)
VALUES 
('123e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000/admin'),
('123e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000/employee'),
('123e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000/client'),
('223e4567-e89b-12d3-a456-426614174001', '223e4567-e89b-12d3-a456-426614174001/admin'),
('223e4567-e89b-12d3-a456-426614174001', '223e4567-e89b-12d3-a456-426614174001/employee'),
('223e4567-e89b-12d3-a456-426614174001', '223e4567-e89b-12d3-a456-426614174001/client');

-- Insertar datos en la tabla 'usuario'
INSERT INTO usuario (id_pasteleria, id_rol, usuario, email, clave_env, nombre, apellido, deshabilitado)
VALUES 
('123e4567-e89b-12d3-a456-426614174000', 11, 'admin_dulce', 'admin@dulcesabor.com', 'clave123', 'Ana', 'Pérez', FALSE),
('123e4567-e89b-12d3-a456-426614174000', 12, 'empleado_dulce', 'empleado@dulcesabor.com', 'clave456', 'Luis', 'García', FALSE),
('223e4567-e89b-12d3-a456-426614174001', 14, 'admin_repostera', 'admin@larepostera.com', 'clave789', 'María', 'López', FALSE),
('223e4567-e89b-12d3-a456-426614174001', 15, 'empleado_repostera', 'empleado@larepostera.com', 'clave321', 'Carlos', 'Hernández', FALSE);

-- Insertar datos en la tabla 'documento'
INSERT INTO documento (id_pasteleria, nombre, bucket)
VALUES 
('123e4567-e89b-12d3-a456-426614174000', 'catalogo', 'catalogos'),
('123e4567-e89b-12d3-a456-426614174000', 'manual', 'manuales'),
('223e4567-e89b-12d3-a456-426614174001', 'catalogo', 'catalogos'),
('223e4567-e89b-12d3-a456-426614174001', 'manual', 'manuales');

-- Insertar datos en la tabla 'base_de_datos'
INSERT INTO base_de_datos (id_pasteleria, nombre, servidor, puerto, usuario, clave)
VALUES 
('123e4567-e89b-12d3-a456-426614174000', 'inventario', 'localhost', '5432', 'admin', 'pass123'),
('123e4567-e89b-12d3-a456-426614174000', 'transacciones', 'localhost', '5432', 'admin', 'pass123'),
('223e4567-e89b-12d3-a456-426614174001', 'inventario', 'localhost', '3306', 'root', 'mysqlpass'),
('223e4567-e89b-12d3-a456-426614174001', 'transacciones', 'localhost', '3306', 'root', 'mysqlpass');

-- Insertar datos en la tabla 'llm'
INSERT INTO llm (id_rol, nombre, modelo, temperatura)
VALUES 
(11, '123e4567-e89b-12d3-a456-426614174000/Admin/GPT-4o', 'gpt-4o', 0),
(12, '123e4567-e89b-12d3-a456-426614174000/Empleado/GPT-4o', 'gpt-4o', 0),
(13, '123e4567-e89b-12d3-a456-426614174000/Cliente/GPT-4o', 'gpt-4o', 0),
(14, '223e4567-e89b-12d3-a456-426614174001/Admin/GPT-4o', 'gpt-4o', 0),
(15, '223e4567-e89b-12d3-a456-426614174001/Empleado/GPT-4o', 'gpt-4o', 0),
(16, '223e4567-e89b-12d3-a456-426614174001/Cliente/GPT-4o', 'gpt-4o', 0);

-- Insertar datos en la tabla 'herramienta'
INSERT INTO herramienta (id_rol, nombre, descripcion)
VALUES 
(11, '123e4567-e89b-12d3-a456-426614174000/Admin/catalogo_doc', 'Useful when you need to anser questions about pastry`s catalog.'),
(11, '123e4567-e89b-12d3-a456-426614174000/Admin/manual_doc', 'Useful when you need to anser questions about to do pastry`s processes.'),
(11, '123e4567-e89b-12d3-a456-426614174000/Admin/inventory_sql_database_agent', 'Useful when you need to answer questions about inventory SQL database.'),
(11, '123e4567-e89b-12d3-a456-426614174000/Admin/transactions_sql_database_agent', 'Useful when you need to answer questions about transactions SQL database.'),
(12, '123e4567-e89b-12d3-a456-426614174000/Empleado/catalogo_doc', 'Useful when you need to anser questions about pastry`s catalog.'),
(12, '123e4567-e89b-12d3-a456-426614174000/Empleado/manual_doc', 'Useful when you need to anser questions about to do pastry`s processes.'),
(13, '123e4567-e89b-12d3-a456-426614174000/Cliente/catalogo_doc', 'Useful when you need to anser questions about pastry`s catalog.'),
(14, '223e4567-e89b-12d3-a456-426614174001/Admin/catalogo_doc', 'Useful when you need to anser questions about pastry`s catalog.'),
(14, '223e4567-e89b-12d3-a456-426614174001/Admin/manual_doc', 'Useful when you need to anser questions about to do pastry`s processes.'),
(14, '223e4567-e89b-12d3-a456-426614174001/Admin/inventory_sql_database_agent', 'Useful when you need to answer questions about inventory SQL database.'),
(14, '223e4567-e89b-12d3-a456-426614174001/Admin/transactions_sql_database_agent', 'Useful when you need to answer questions about transactions SQL database.'),
(15, '223e4567-e89b-12d3-a456-426614174001/Empleado/catalogo_doc', 'Useful when you need to anser questions about pastry`s catalog.'),
(15, '223e4567-e89b-12d3-a456-426614174001/Empleado/manual_doc', 'Useful when you need to anser questions about to do pastry`s processes.'),
(16, '223e4567-e89b-12d3-a456-426614174001/Cliente/catalogo_doc', 'Useful when you need to anser questions about pastry`s catalog.');
