-- Crear la tabla 'pasteleria'
CREATE TABLE pasteleria (
    id UUID PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    telefono VARCHAR,
    direccion VARCHAR,
    ciudad VARCHAR,
    codigo_postal VARCHAR,
    url_website VARCHAR,
    fecha_registro DATE
);

-- Crear la tabla 'documento'
CREATE TABLE documento (
    id SERIAL PRIMARY KEY,
    id_pasteleria UUID REFERENCES pasteleria(id),
    nombre VARCHAR NOT NULL,
    bucket VARCHAR NOT NULL
);

-- Crear la tabla 'base_de_datos'
CREATE TABLE base_de_datos (
    id SERIAL PRIMARY KEY,
    id_pasteleria UUID REFERENCES pasteleria(id),
    nombre VARCHAR NOT NULL,
    servidor VARCHAR NOT NULL,
    puerto VARCHAR NOT NULL,
    usuario VARCHAR NOT NULL,
    clave VARCHAR NOT NULL
);

-- Crear la tabla 'rol'
CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    id_pasteleria UUID REFERENCES pasteleria(id),
    nombre VARCHAR UNIQUE NOT NULL
);

-- Crear la tabla 'usuario'
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    id_pasteleria UUID REFERENCES pasteleria(id),
    id_rol INT REFERENCES rol(id),
    usuario VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    clave_env VARCHAR NOT NULL,
    nombre VARCHAR,
    apellido VARCHAR,
    deshabilitado BOOLEAN DEFAULT FALSE
);

-- Crear la tabla 'llm'
CREATE TABLE llm (
    id SERIAL PRIMARY KEY,
    id_rol INT REFERENCES rol(id),
    nombre VARCHAR UNIQUE NOT NULL,
    modelo VARCHAR NOT NULL,
    temperatura DOUBLE PRECISION
);

-- Crear la tabla 'prompt'
CREATE TABLE prompt (
    id SERIAL PRIMARY KEY,
    id_rol INT REFERENCES rol(id),
    template VARCHAR NOT NULL
);

-- Crear la tabla 'herramienta'
CREATE TABLE herramienta (
    id SERIAL PRIMARY KEY,
    id_rol INT REFERENCES rol(id),
    nombre VARCHAR UNIQUE NOT NULL,
    descripcion VARCHAR
);
