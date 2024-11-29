CREATE TABLE IF NOT EXISTS precios (
    id_precio SERIAL PRIMARY KEY,
    tipo_destino VARCHAR(60),
    duracion INT,
    transporte BOOLEAN,
    sup_hab_ind INT,
    precio INT
);

CREATE TABLE IF NOT EXISTS destinos (
    id_destino SERIAL PRIMARY KEY,
    destino VARCHAR(60),
    tipo_destino VARCHAR(60)
);

CREATE TABLE IF NOT EXISTS viajes (
    id_viaje SERIAL PRIMARY KEY,
    id_destino INTEGER,
    id_precio INTEGER,
    FOREIGN KEY (id_destino) REFERENCES destinos (id_destino),
    FOREIGN KEY (id_precio) REFERENCES precios (id_precio)
);

CREATE TABLE IF NOT EXISTS datos (
    id_solicitante SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS anyos_ant (
    id_solicitante SERIAL PRIMARY KEY,
    lista_espera BOOLEAN,
    viaje_2021 BOOLEAN,
    viaje_2022 BOOLEAN,
    num_max_viaje_por_temp INT,
    FOREIGN KEY (id_solicitante) REFERENCES datos (id_solicitante)
);

CREATE TABLE IF NOT EXISTS caract (
    id_caract SERIAL PRIMARY KEY,
    id_solicitante INTEGER,
    sexo VARCHAR(20),
    edad INT,
    trabajo VARCHAR(50),
    anyos_trabajados INT,
    movilidad VARCHAR(20),
    discapacidad BOOLEAN,
    enfermedad BOOLEAN,
    FOREIGN KEY (id_solicitante) REFERENCES datos (id_solicitante)
);

CREATE TABLE IF NOT EXISTS fam_num (
    id_fam_num SERIAL PRIMARY KEY,
    id_solicitante INTEGER,
    familia_numerosa BOOLEAN,
    edad_hijo INT,
    trabaja_hijo BOOLEAN,
    FOREIGN KEY (id_solicitante) REFERENCES datos (id_solicitante)
);

CREATE TABLE IF NOT EXISTS habitacion (
    id_habitacion SERIAL PRIMARY KEY,
    id_solicitante INTEGER,
    hab_ind BOOLEAN,
    FOREIGN KEY (id_solicitante) REFERENCES datos (id_solicitante)
);

CREATE TABLE IF NOT EXISTS pensiones (
    id_pensiones SERIAL PRIMARY KEY,
    id_solicitante INTEGER,
    renta INT,
    pension INT,
    tipo_pension VARCHAR(10),
    estado_civil VARCHAR(10),
    pension_conyuge INT,
    FOREIGN KEY (id_solicitante) REFERENCES datos (id_solicitante)
);

CREATE TABLE IF NOT EXISTS viajero (
    id_viajero SERIAL PRIMARY KEY,
    id_solicitante INTEGER,
    domicilio VARCHAR(30),
    vehiculo BOOLEAN,
    FOREIGN KEY (id_solicitante) REFERENCES datos (id_solicitante)
);

CREATE TABLE IF NOT EXISTS solicitudes (
    id_solicitud SERIAL PRIMARY KEY,
    id_solicitante INTEGER,
    id_viaje INTEGER,
    solicita_menu BOOLEAN,
    FOREIGN KEY (id_solicitante) REFERENCES datos (id_solicitante),
    FOREIGN KEY (id_viaje) REFERENCES viajes (id_viaje)
);

CREATE TABLE IF NOT EXISTS mes (
    id_mes_viaje SERIAL PRIMARY KEY,
    id_viaje INTEGER,
    mes VARCHAR(20),
    posibilidad_menu BOOLEAN,
    FOREIGN KEY (id_viaje) REFERENCES viajes (id_viaje)
);