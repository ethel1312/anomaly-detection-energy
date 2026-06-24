CREATE TABLE usuario( 
    idusuario INT AUTO_INCREMENT PRIMARY KEY, 
    nombre VARCHAR(100) NOT NULL, 
    correo VARCHAR(100) UNIQUE NOT NULL, 
    password VARCHAR(255) NOT NULL, 
    rol ENUM('analista','supervisor','jefe') NOT NULL DEFAULT 'analista', 
    estado TINYINT(1) DEFAULT 1, -- 1=activo, 0=inactivo 
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE analisis(
    idanalisis INT AUTO_INCREMENT PRIMARY KEY,
    idusuario INT NOT NULL,
    nombre_archivo VARCHAR(255) NOT NULL,
    total_registros INT NOT NULL,
    total_anomalias INT NOT NULL,
    porcentaje_anomalias DECIMAL(5,2),
    fecha_proceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idusuario)
        REFERENCES usuario(idusuario)
);

CREATE TABLE resultado_prediccion(
    idresultado INT AUTO_INCREMENT PRIMARY KEY,
    idanalisis INT NOT NULL,
    cons_no VARCHAR(100) NOT NULL,
    probabilidad DECIMAL(8,2) NOT NULL,
    estado ENUM(
        'NORMAL',
        'ANOMALO'
    ) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idanalisis)
        REFERENCES analisis(idanalisis)
);

CREATE TABLE alerta(
    idalerta INT AUTO_INCREMENT PRIMARY KEY,
    idresultado INT NOT NULL,
    prioridad ENUM(
        'BAJA',
        'MEDIA',
        'ALTA'
    ) NOT NULL,
    descripcion VARCHAR(255),
    estado ENUM(
        'PENDIENTE',
        'REVISADA'
    ) DEFAULT 'PENDIENTE',
    fecha_alerta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idresultado)
        REFERENCES resultado_prediccion(idresultado)
);

ALTER TABLE alerta
ADD COLUMN resultado_revision ENUM(
    'FRAUDE_CONFIRMADO',
    'FALSA_ALERTA'
) NULL;

ALTER TABLE resultado_prediccion
ADD COLUMN patron VARCHAR(255);

ALTER TABLE resultado_prediccion
ADD COLUMN consumo_promedio DECIMAL(10,2);

ALTER TABLE resultado_prediccion
ADD COLUMN consumo_ratio DECIMAL(10,2);

ALTER TABLE resultado_prediccion
ADD COLUMN consumo_desviacion DECIMAL(10,2);