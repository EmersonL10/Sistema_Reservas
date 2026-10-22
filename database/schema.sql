-- ACT-04: esquema inicial del Sistema de Reservas.
-- Ejecutar las conexiones de la aplicación con zona horaria UTC.
-- Este script no elimina bases ni tablas existentes.

CREATE DATABASE IF NOT EXISTS sistema_reservas
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

USE sistema_reservas;

CREATE TABLE clientes (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(120) NOT NULL,
    telefono VARCHAR(30) NOT NULL,
    email VARCHAR(254) NULL,
    creado_en DATETIME(6) NOT NULL DEFAULT (UTC_TIMESTAMP(6)),
    actualizado_en DATETIME(6) NULL,

    PRIMARY KEY (id),
    CONSTRAINT chk_cliente_nombre
        CHECK (CHAR_LENGTH(TRIM(nombre)) > 0),
    CONSTRAINT chk_cliente_telefono
        CHECK (CHAR_LENGTH(TRIM(telefono)) > 0)
) ENGINE = InnoDB;

CREATE TABLE servicios (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(120) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    duracion_minutos SMALLINT UNSIGNED NOT NULL,
    creado_en DATETIME(6) NOT NULL DEFAULT (UTC_TIMESTAMP(6)),

    PRIMARY KEY (id),
    CONSTRAINT chk_servicio_nombre
        CHECK (CHAR_LENGTH(TRIM(nombre)) > 0),
    CONSTRAINT chk_servicio_precio
        CHECK (precio >= 0),
    CONSTRAINT chk_servicio_duracion
        CHECK (duracion_minutos > 0)
) ENGINE = InnoDB;

CREATE TABLE agenda (
    id TINYINT UNSIGNED NOT NULL,
    nombre VARCHAR(80) NOT NULL,

    PRIMARY KEY (id),
    CONSTRAINT chk_agenda_unica CHECK (id = 1)
) ENGINE = InnoDB;

INSERT INTO agenda (id, nombre)
VALUES (1, 'Agenda principal');

CREATE TABLE reservas (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    agenda_id TINYINT UNSIGNED NOT NULL DEFAULT 1,
    cliente_id BIGINT UNSIGNED NOT NULL,
    servicio_id BIGINT UNSIGNED NOT NULL,
    inicio_utc DATETIME(6) NOT NULL,
    fin_utc DATETIME(6) NOT NULL,
    precio_aplicado DECIMAL(10,2) NOT NULL,
    duracion_aplicada_minutos SMALLINT UNSIGNED NOT NULL,
    estado VARCHAR(12) NOT NULL DEFAULT 'Confirmada',
    creado_en DATETIME(6) NOT NULL DEFAULT (UTC_TIMESTAMP(6)),
    cancelado_en DATETIME(6) NULL,

    PRIMARY KEY (id),

    CONSTRAINT fk_reserva_agenda
        FOREIGN KEY (agenda_id) REFERENCES agenda (id)
        ON DELETE RESTRICT ON UPDATE RESTRICT,

    CONSTRAINT fk_reserva_cliente
        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        ON DELETE RESTRICT ON UPDATE RESTRICT,

    CONSTRAINT fk_reserva_servicio
        FOREIGN KEY (servicio_id) REFERENCES servicios (id)
        ON DELETE RESTRICT ON UPDATE RESTRICT,

    CONSTRAINT chk_reserva_intervalo
        CHECK (fin_utc > inicio_utc),

    CONSTRAINT chk_reserva_precio
        CHECK (precio_aplicado >= 0),

    CONSTRAINT chk_reserva_duracion
        CHECK (
            duracion_aplicada_minutos > 0
            AND fin_utc = TIMESTAMPADD(
                MINUTE, duracion_aplicada_minutos, inicio_utc
            )
        ),

        CONSTRAINT chk_reserva_estado
        CHECK (
            CAST(estado AS BINARY) IN (
                CAST('Confirmada' AS BINARY),
                CAST('Cancelada' AS BINARY)
            )
        ),

    CONSTRAINT chk_reserva_cancelacion
        CHECK (
            (CAST(estado AS BINARY) = CAST('Confirmada' AS BINARY)
                AND cancelado_en IS NULL)
            OR
            (CAST(estado AS BINARY) = CAST('Cancelada' AS BINARY)
                AND cancelado_en IS NOT NULL)
        ),

    INDEX idx_reserva_disponibilidad (
        agenda_id, estado, inicio_utc, fin_utc
    ),
    INDEX idx_reserva_cliente (cliente_id),
    INDEX idx_reserva_servicio (servicio_id)
) ENGINE = InnoDB;
