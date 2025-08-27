DROP DATABASE IF EXISTS satelites_db;
CREATE DATABASE satelites_db;
USE satelites_db;

CREATE TABLE Satelite (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    fecha_lanzamiento DATE,
    orbita VARCHAR(50),
    estado VARCHAR(50)
);

CREATE TABLE Sensor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    satelite_id INT,
    nombre VARCHAR(100),
    tipo_unidad VARCHAR(50),
    FOREIGN KEY (satelite_id) REFERENCES Satelite(id) ON DELETE CASCADE
);

CREATE TABLE Mision (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    satelite_id INT,
    objetivo VARCHAR(255),
    zona VARCHAR(255),
    duracion INT(7),
    estado VARCHAR(50),
    FOREIGN KEY (satelite_id) REFERENCES Satelite(id) ON DELETE CASCADE
);

CREATE TABLE datos_mision (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_mision INT NOT NULL,
    id_sensor INT NOT NULL,
    valor INT NOT NULL,
    FOREIGN KEY (id_mision) REFERENCES Mision(id) ON DELETE CASCADE,
    FOREIGN KEY (id_sensor) REFERENCES Sensor(id) ON DELETE CASCADE
);
