DROP DATABASE IF EXISTS satelites_db;
CREATE DATABASE satelites_db;
USE satelites_db;

CREATE TABLE Satelites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    fecha_lanzamiento DATE,
    orbita VARCHAR(50),
    estado VARCHAR(50)
);

CREATE TABLE Sensores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    satelite_id INT,
    nombre VARCHAR(100),
    tipo_unidad VARCHAR(50),
    FOREIGN KEY (satelite_id) REFERENCES Satelites(id) ON DELETE CASCADE
);

CREATE TABLE Misiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    satelite_id INT,
    objetivo VARCHAR(255),
    zona VARCHAR(255),
    duracion INT(7),
    estado VARCHAR(50),
    FOREIGN KEY (satelite_id) REFERENCES Satelites(id) ON DELETE CASCADE
);
