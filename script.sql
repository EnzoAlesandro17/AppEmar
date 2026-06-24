CREATE TABLE Categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE Productos (
    codigo VARCHAR(50) PRIMARY KEY,
    id_categoria INT,
    descripcion TEXT,
    precio_may DECIMAL(10, 2),
    precio_min DECIMAL(10, 2),
    stock INT DEFAULT 0,
    FOREIGN KEY (id_categoria) REFERENCES Categorias(id)
);

CREATE TABLE Celulares (
    codigo VARCHAR(50) PRIMARY KEY,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    rom VARCHAR(20),
    ram VARCHAR(20),
	precio DECIMAL(10, 2),
);

CREATE TABLE Colores (
    id INT PRIMARY KEY,
    codigo_celular VARCHAR(50),
    color VARCHAR(30) NOT NULL,
    FOREIGN KEY (codigo_celular) REFERENCES Celulares(codigo)
);

CREATE TABLE IMEIs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_color INT,
    numero_imei VARCHAR(15) UNIQUE NOT NULL,
    FOREIGN KEY (id_color) REFERENCES Colores(id)
);

