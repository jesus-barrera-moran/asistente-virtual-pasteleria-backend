CREATE TABLE Categorias (
    categoria_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

CREATE TABLE Productos (
    producto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    categoria_id INT NOT NULL,
    cantidad_stock INT NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES Categorias(categoria_id)
);

CREATE TABLE Proveedores (
    proveedor_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(100),
    direccion TEXT
);

CREATE TABLE Ingredientes (
    ingrediente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    unidad_medida VARCHAR(50) NOT NULL,
    cantidad_stock INT NOT NULL,
    proveedor_id INT NOT NULL,
    FOREIGN KEY (proveedor_id) REFERENCES Proveedores(proveedor_id)
);

INSERT INTO Categorias (nombre, descripcion) VALUES
('Pasteles', 'Diferentes tipos de pasteles'),
('Galletas', 'Variedades de galletas'),
('Pan', 'Diferentes tipos de pan'),
('Postres', 'Variedad de postres');

INSERT INTO Proveedores (nombre, contacto, direccion) VALUES
('Proveedor A', 'contacto@proveedora.com', 'Calle 123, Ciudad A'),
('Proveedor B', 'contacto@proveedorb.com', 'Avenida 456, Ciudad B'),
('Proveedor C', 'contacto@proveedorc.com', 'Carretera 789, Ciudad C');

INSERT INTO Productos (nombre, descripcion, precio, categoria_id, cantidad_stock) VALUES
('Pastel de Chocolate', 'Pastel de chocolate con cobertura de chocolate', 15.99, 1, 20),
('Galletas de Avena', 'Galletas saludables de avena', 5.49, 2, 50),
('Pan Integral', 'Pan saludable integral', 2.99, 3, 30),
('Tarta de Manzana', 'Tarta de manzana con canela', 12.99, 4, 15);

INSERT INTO Ingredientes (nombre, descripcion, unidad_medida, cantidad_stock, proveedor_id) VALUES
('Harina', 'Harina de trigo para hornear', 'kg', 100, 1),
('Azúcar', 'Azúcar blanca refinada', 'kg', 50, 2),
('Huevos', 'Huevos frescos de granja', 'unidad', 200, 1),
('Leche', 'Leche entera pasteurizada', 'litro', 60, 3),
('Mantequilla', 'Mantequilla sin sal', 'kg', 25, 2),
('Chocolate', 'Chocolate amargo para repostería', 'kg', 40, 3),
('Avena', 'Avena en hojuelas', 'kg', 30, 1),
('Manzanas', 'Manzanas frescas para tarta', 'kg', 20, 3);
