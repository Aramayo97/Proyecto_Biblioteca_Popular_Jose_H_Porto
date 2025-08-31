CREATE DATABASE IF NOT EXISTS biblioteca;
USE biblioteca;

-- Tabla socios
CREATE TABLE IF NOT EXISTS socios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    apellido VARCHAR(100),
    nombre VARCHAR(100),
    dni VARCHAR(15),
    domicilio VARCHAR(200),
    ultimop DATE,
    telefono VARCHAR(20),
    sexo VARCHAR(10)
);

-- Tabla libros
CREATE TABLE IF NOT EXISTS libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20),
    titulo VARCHAR(200),
    categoria VARCHAR(100),
    subcategoria VARCHAR(100),
    autor VARCHAR(100),
    editorial VARCHAR(100),
    descripcion TEXT,
    disponible BOOLEAN DEFAULT TRUE
);

-- Tabla prestamos
CREATE TABLE IF NOT EXISTS prestamos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    socio_id INT,
    libro_id INT,
    fecha_prestamo DATE,
    fecha_devolucion DATE,
    devuelto BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (socio_id) REFERENCES socios(id),
    FOREIGN KEY (libro_id) REFERENCES libros(id)
);