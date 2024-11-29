import pandas as pd
import numpy as np
import random
import psycopg2
import time
import unidecode
from gender_guesser.detector import Detector
from faker import Faker

for i in range(1,2):
    time.sleep(10)

conn = psycopg2.connect(host='postgres', dbname='project', user='project', password ='project')
cur = conn.cursor()

fake = Faker('es_ES')
nombres_con_acentos = [fake.first_name() for _ in range(50000)]
apellidos_con_acentos = [fake.last_name() for _ in range(50000)]
nombres_sin_acentos = [unidecode.unidecode(nombre) for nombre in nombres_con_acentos]
apellidos_sin_acentos = [unidecode.unidecode(apellido) for apellido in apellidos_con_acentos]
data = {'nombre': nombres_sin_acentos, 'apellido': apellidos_sin_acentos}
df_datos = pd.DataFrame(data)
df_datos['id_solicitante'] = df_datos.index + 1
df_datos = df_datos[['id_solicitante','nombre','apellido']]

datos_values = df_datos[['id_solicitante', 'nombre', 'apellido']].values.tolist()
cur.executemany(
    "INSERT INTO datos (id_solicitante, nombre, apellido) VALUES (%s, %s, %s)",
    datos_values
)

df_caract = df_datos.copy()
df_caract['sexo'] = None
df_caract['edad'] = np.random.randint(65, 100, len(df_caract))
df_caract['trabajo'] = None
df_caract['movilidad'] = np.random.choice(['perfecta', 'media', 'limitada'], len(df_caract))
df_caract['discapacidad'] = np.random.choice([True, False], len(df_caract))
df_caract['enfermedad'] = np.random.choice([False] * 99 + [True], len(df_caract))
df_caract['anyos_trabajados'] = np.random.randint(15, 41, len(df_caract))

gender_detector = Detector()
def get_gender(name):
    return gender_detector.get_gender(name)
df_caract['sexo'] = df_caract['nombre'].apply(get_gender)

trabajos = [
    "Medico", "Enfermero", "Profesor", "Ingeniero", "Abogado", "Arquitecto", "Administrativo",
    "Comercial/Vendedor", "Electricista", "Fontanero", "Programador_informatico", "Diseñador_grafico",
    "Carpintero", "Cocinero", "Camarero", "Agricultor", "Peluquero", "Fontanero",
    "Operario_de_fabrica"
]

df_caract['trabajo'] = np.random.choice(trabajos, len(df_caract))
df_caract['id_caract'] = df_caract['id_solicitante']

df_caract['discapacidad'] = np.random.choice([True, False], len(df_caract))
df_caract['discapacidad'].fillna(False, inplace=True)
df_caract['discapacidad'] = df_caract['discapacidad'].astype(bool)

df_caract['enfermedad'] = np.random.choice([True, False], len(df_caract))
df_caract['enfermedad'].fillna(False, inplace=True)
df_caract['enfermedad'] = df_caract['enfermedad'].astype(bool)

df_caract = df_caract[['id_caract','id_solicitante', 'sexo', 'edad', 'trabajo', 'anyos_trabajados',
       'movilidad', 'discapacidad', 'enfermedad']]

caract_values = df_caract[['id_caract', 'id_solicitante', 'sexo', 'edad', 'trabajo', 'anyos_trabajados', 'movilidad', 'discapacidad', 'enfermedad']].values.tolist()
cur.executemany(
    "INSERT INTO caract (id_caract, id_solicitante, sexo, edad, trabajo, anyos_trabajados, movilidad, discapacidad, enfermedad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    caract_values
)

df_viajero = df_datos.copy()
destinos_cap = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", "Malaga", "Murcia",
    "Palma de Mallorca", "Las Palmas de Gran Canaria", "Bilbao", "Alicante", "Córdoba",
    "Valladolid", "Vigo", "Girona", "Lugo", "León", "Toledo", "Santander", "Pamplona",
    "Logrono", "Badajoz", "Huesca", "Castellon de la Plana", "Tarragona", "Lleida",
    "Ourense", "Caceres", "Jaen", "Almeria", "Ciudad Real", "Huelva", "Cuenca", "Avila",
    "Segovia", "Soria", "Teruel", "Cuenca", "Zamora", "Guadalajara", "Palencia", "Huesca"]
dest1 = destinos_cap * 80

destinos_nocap = ["Avila", "Salamanca", "Caceres", "Oviedo", "Soria", "Girona", "Pontevedra", "Ronda", "Cudillero", 
    "Albarracin", "Cudillero", "Alcala del Jucar", "Combarro", 
    "Frigiliana", "Ainsa", "Peniscola", "Trujillo", "Besalu", "Valderrobres", 
    "Almagro", "Ujue", "Mirambel", "Morella", "La Alberca", "Chinchon", 
    "Sepulveda", "Calaceite", "Albarracin", "Mogarraz", "Frias", 
    "Poza de la Sal", "Valverde de los Arroyos", "Santillana del Mar", 
    "Barcena Mayor", "Vilafames", "Medinaceli", "Alquezar", "Yanguas", 
    "Monteagudo de las Vicarias", "Ujue", "Candelario", "Fornalutx", 
    "Cadaques", "Valldemossa", "Ainsa", "Pals", "Mogarraz", "Pedraza", 
    "Lerma", "Penalba de Santiago", "Almagro", "Frias", "Valldemossa", 
    "Alcala del Júcar", "Aracena", "Chinchon", "Caleruega"]
dest2 = destinos_nocap * 20
domicilio = dest1 + dest2

df_viajero['domicilio'] = np.random.choice(domicilio, len(df_viajero))
df_viajero['vehiculo'] = np.random.choice([True, False], len(df_viajero))
df_viajero['vehiculo'].fillna(False, inplace=True)
df_viajero['vehiculo'] = df_viajero['vehiculo'].astype(bool)
df_viajero = df_viajero[['id_solicitante', 'domicilio', 'vehiculo']]


viajero_values = df_viajero[['id_solicitante', 'domicilio', 'vehiculo']].values.tolist()
cur.executemany(
    "INSERT INTO viajero (id_solicitante, domicilio, vehiculo) VALUES (%s, %s, %s)",
    viajero_values
)

df_fam_num = df_datos.copy()
df_fam_num['familia_numerosa'] = np.random.choice([True, False], size=len(df_fam_num))
df_fam_num['edad_hijo'] = np.where(df_fam_num['familia_numerosa'], np.random.randint(15, 26, size=len(df_fam_num)), None)
df_fam_num['trabaja_hijo'] = np.where((df_fam_num['familia_numerosa']) & (df_fam_num['edad_hijo'] > 20), True, None)
df_fam_num['edad_hijo'].fillna(False, inplace=True)
df_fam_num['trabaja_hijo'].fillna(False, inplace=True)
df_fam_num['edad_hijo'] = df_fam_num['edad_hijo'].replace(False, 0)
df_fam_num['edad_hijo'] = pd.to_numeric(df_fam_num['edad_hijo'], errors='coerce')
df_fam_num['trabaja_hijo'] = df_fam_num['trabaja_hijo'].astype(bool)

fam_num_values = df_fam_num[['id_solicitante', 'familia_numerosa', 'edad_hijo', 'trabaja_hijo']].values.tolist()
cur.executemany(
    "INSERT INTO fam_num (id_solicitante, familia_numerosa, edad_hijo, trabaja_hijo) VALUES (%s, %s, %s, %s)",
    fam_num_values
)

df = df_datos.copy()
df_pensiones = df[['id_solicitante']].copy()
rentas = [0, 8400, 12000, 15000, 18000, 21000]
df_pensiones['renta'] = np.random.choice(rentas, len(df_pensiones))
df_pensiones['pension'] = np.random.randint(6784.54, 42830.29, len(df_pensiones))

bins = [6774.54, 12600, 14700, 16800, 18900, 21000, 23100, 25200, 27300, 29400, float('inf')]
etiquetas = ['tipo_1', 'tipo_2', 'tipo_3', 'tipo_4', 'tipo_5', 'tipo_6', 'tipo_7', 'tipo_8', 'tipo_9', 'tipo_10']
df_pensiones['tipo_pension'] = pd.cut(df_pensiones['pension'], bins=bins, labels=etiquetas)

estados = ['soltero/a', 'casado/a', 'viudo/a']
df_pensiones['estado_civil'] = np.random.choice(estados, len(df_pensiones))
df_pensiones.loc[df_pensiones['estado_civil'] == 'casado/a', 'pension_conyuge'] = np.random.randint(6784.54, 42830.29, df_pensiones['estado_civil'].eq('casado/a').sum())
df_pensiones['pension_conyuge'] .fillna(0, inplace=True)
df_pensiones['pension_conyuge'] = df_pensiones['pension_conyuge'].astype(float)
df_pensiones['pension_conyuge'] = df_pensiones['pension_conyuge'].astype(int)

pensiones_values = df_pensiones[['id_solicitante', 'renta', 'pension', 'tipo_pension', 'estado_civil', 'pension_conyuge']].values.tolist()
cur.executemany(
    "INSERT INTO pensiones (id_solicitante, renta, pension, tipo_pension, estado_civil, pension_conyuge) VALUES (%s, %s, %s, %s, %s, %s)",
    pensiones_values
)

df_años_ant = df.copy()
df_años_ant['lista_espera'] = np.random.choice([True, False], len(df_años_ant))
df_años_ant['viaje_2021'] = np.random.choice([True, False], len(df_años_ant))
df_años_ant['viaje_2022'] = np.random.choice([True, False], len(df_años_ant))
df_años_ant['num_max_viaje_por_temp'] = np.random.randint( 1, 4, len(df_años_ant))
df_años_ant

años_ant_values = df_años_ant[['id_solicitante', 'lista_espera', 'viaje_2021', 'viaje_2022', 'num_max_viaje_por_temp']].values.tolist()
cur.executemany(
    "INSERT INTO anyos_ant (id_solicitante, lista_espera, viaje_2021, viaje_2022, num_max_viaje_por_temp) VALUES (%s, %s, %s, %s, %s)",
    años_ant_values
)

df_habitacion = df.copy()
df_habitacion['hab_ind'] = np.random.choice(([True] * 25 + [False] * 75), len(df_habitacion))
df_habitacion['hab_ind'].fillna(False, inplace=True)
df_habitacion['hab_ind'] = df_habitacion['hab_ind'].astype(bool)
df_habitacion = df_habitacion[['id_solicitante', 'hab_ind']]

habitacion_values = df_habitacion[['id_solicitante', 'hab_ind']].values.tolist()
cur.executemany(
    "INSERT INTO habitacion (id_solicitante, hab_ind) VALUES (%s, %s)",
    habitacion_values
)


zona_costera = ["Ruta_Andalucia", "Ruta_Cataluña", "Ruta_Murcia", "Ruta_CV"]
zona_baleares = ["Ruta_Baleares"]
zona_canarias = ["Ruta_Canarias"]

circuitos_culturales = [
    "Jerez de la Frontera", "Cordoba", "Albolote", "Granada", "Jaen", "Benalmadena", 
    "Sevilla", "Huesca", "Teruel", "Zaragoza", "Gijon", "Oviedo", "Palma de Mallorca", 
    "Las Palmas de Gran Canaria", "Santander", "Santoña", "Suances", "Torrelavega", 
    "Ciudad Real", "Cuenca", "Guadalajara", "Toledo", "Avila", "Burgos", "Leon", 
    "Palencia", "Salamanca", "Segovia", "Soria", "Valladolid", "Zamora", "Barcelona", 
    "Tarragona", "Alicante", "Castellon", "Valencia", "Badajoz", "Caceres", "A Coruña", 
    "Lugo", "Ourense", "Sanxenxo", "Haro", "Logroño", "Aranjuez", "Pinto", 
    "San Lorenzo del Escorial", "Aguilas", "La Manga del Mar Menor", "Pamplona", "Burguete", 
    "Laguardia", "Eibar", "Sondika", "Ceuta", "Melilla"
]

turismo_naturaleza = [
    "Aguadulce", "Sanlucar de Barrameda", "Islantilla y Punta Umbria", 
    "La Iruela y Villanueva del Arzobispo", "Barbastro", "Gijon_2", "Palma de Mallorca_2", 
    "Las Palmas de Gran Canaria_2", "Puerto de la Cruz", "Cabuerniga", "Hellin", "Cuenca_2", 
    "Avila_2", "Mogarraz", "Soria_2", "Pont de Suert", "Peñiscola", "Trujillo", 
    "Santiago de Compostela", "Haro_2", "San Lorenzo del Escorial_2", "Zarautz"
]

capitales_provincia = [
    "Cordoba_2", "Granada_2", "Sevilla_2", "Zaragoza_2", "Santander_2", "Toledo_2", 
    "Burgos_2", "Leon_2", "Salamanca_2", "Zamora_2", "Girona", "Valencia_2", "Caceres_2", 
    "Ourense_2", "San Sebastian"
]

ceuta_melilla = ["Ceuta_2", "Melilla_2"]

destinos = zona_costera + zona_baleares + zona_canarias + circuitos_culturales + turismo_naturaleza + capitales_provincia + ceuta_melilla
destinos = pd.Series(destinos)
df_destinos = pd.DataFrame(destinos, columns=['destino'])

df_destinos.index = range(1, len(df_destinos) + 1)
df_destinos['id_destino'] = df_destinos.index
df_destinos['tipo_destino'] = 'zona_costera'  

df_destinos.loc[:4, 'tipo_destino'] = 'zona_costera'
df_destinos.loc[5, 'tipo_destino'] = 'zona_baleares'
df_destinos.loc[6, 'tipo_destino'] = 'zona_canarias'
df_destinos.loc[7:62, 'tipo_destino'] = 'circuitos_culturales'
df_destinos.loc[63:84, 'tipo_destino'] = 'turismo_naturaleza'
df_destinos.loc[85:99, 'tipo_destino'] = 'capitales_provincia'
df_destinos.loc[100:, 'tipo_destino'] = 'viaje_ceuta_melilla'

df_destinos = df_destinos[['id_destino', 'destino', 'tipo_destino']]

destinos_values = df_destinos[['id_destino', 'destino', 'tipo_destino']].values.tolist()
cur.executemany(
    "INSERT INTO destinos (id_destino, destino, tipo_destino) VALUES (%s, %s, %s)",
    destinos_values
)

df_precios = pd.DataFrame({
    'id_precio': np.random.randint(1,100,16)
})
df_precios.index = range(1, len(df_precios) + 1)
df_precios['id_precio'] = df_precios.index


df_precios.loc[:4, 'tipo_destino'] = 'zona_costera'
df_precios.loc[5:8, 'tipo_destino'] = 'zona_baleares'
df_precios.loc[9:12, 'tipo_destino'] = 'zona_canarias'
df_precios.loc[13, 'tipo_destino'] = 'circuitos_culturales'
df_precios.loc[14, 'tipo_destino'] = 'turismo_naturaleza'
df_precios.loc[15, 'tipo_destino'] = 'capitales_provincia'
df_precios.loc[16, 'tipo_destino'] = 'viaje_ceuta_melilla'

duraciones = [7,9,7,9,7,9,7,9,7,9,7,9,5,4,3,4]
df_precios['duracion'] = duraciones
df_precios['transporte'] = True
indices_false = [2,3,6,7,10,11]
df_precios.loc[indices_false, 'transporte'] = False

suplemento_hab_indv = [22,22,22,22,22,22,22,22,24,24,24,24,26,26,26,26]
df_precios['sup_hab_ind'] = suplemento_hab_indv

precios = [228.93, 253.65, 210.72, 290.07, 267.63, 253.77, 210.47, 331.49,
           355.30, 253.65, 210.39, 435.95, 293.16, 286.82, 124.68, 286.82]

df_precios['precio'] = precios

precios_values = df_precios[['id_precio', 'tipo_destino', 'duracion', 'transporte', 'sup_hab_ind', 'precio']].values.tolist()
cur.executemany(
    "INSERT INTO precios (id_precio, tipo_destino, duracion, transporte, sup_hab_ind, precio) VALUES (%s, %s, %s, %s, %s, %s)",
    precios_values
)

df_viajes = pd.DataFrame({
    'id_viaje': np.random.randint(1,5,5000)
})
df_viajes.index = range(1, len(df_viajes) + 1)
df_viajes['id_viaje'] = df_viajes.index
df_viajes['destino'] = np.random.choice(destinos, len(df_viajes))
mapeo_ids = df_destinos.set_index('destino')['id_destino']
df_viajes['id_destino'] = df_viajes['destino'].map(mapeo_ids)

mapeo_tipo = df_destinos.set_index('destino')['tipo_destino']
df_viajes['tipo_destino'] = df_viajes['destino'].map(mapeo_tipo)

def asignar_precio(row):
    if row['tipo_destino'] == 'turismo_naturaleza':
        return 14
    elif row['tipo_destino'] == 'circuitos_culturales':
        return 13
    elif row['tipo_destino'] == 'capitales_provincia':
        return 15
    elif row['tipo_destino'] == 'viaje_ceuta_melilla':
        return 16
    elif row['tipo_destino'] == 'zona_canarias':
        return np.random.randint(9, 13)
    elif row['tipo_destino'] == 'zona_baleares':
        return np.random.randint(5, 9)
    elif row['tipo_destino'] == 'zona_costera':
        return np.random.randint(1, 5)

df_viajes['id_precio'] = df_viajes.apply(asignar_precio, axis=1)

df_viajes = df_viajes[['id_viaje', 'id_destino', 'id_precio']]

viajes_values = df_viajes[['id_viaje', 'id_destino', 'id_precio']].values.tolist()
cur.executemany(
    "INSERT INTO viajes (id_viaje, id_destino, id_precio) VALUES (%s, %s, %s)",
    viajes_values
)

df_mes = df_viajes[['id_viaje']].copy()
meses = ['octubre', 'noviembre', 'diciembre', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio']
df_mes['mes'] = np.random.choice(meses, len(df_mes))
df_mes['posibilidad_menu'] = np.where((df_mes['mes'] == 'diciembre') | (df_mes['mes'] == 'mayo'), True, False)

mes_values = df_mes[['id_viaje', 'mes', 'posibilidad_menu']].values.tolist()
cur.executemany(
    "INSERT INTO mes (id_viaje, mes, posibilidad_menu) VALUES (%s, %s, %s)",
    mes_values
)

df_solicitantes = df.copy()
def obtener_4_viajes():
    return np.random.choice(df_viajes['id_viaje'], size=4, replace=True)

df_solicitantes['ids_viajes'] = df_solicitantes.apply(lambda x: obtener_4_viajes(), axis=1)
df_solicitantes = df_solicitantes.explode('ids_viajes')
df_solicitantes2 = pd.merge(df_solicitantes, df_viajes, left_on='ids_viajes', right_on='id_viaje')
df_solicitantes2 = df_solicitantes2[['id_solicitante', 'id_viaje']]
mapping = df_mes.set_index('id_viaje')['posibilidad_menu'].to_dict()
df_solicitantes2['posibilidad_menu'] = df_solicitantes2['id_viaje'].map(mapping)
df_solicitantes2['solicita_menu'] = False
mask = df_solicitantes2['posibilidad_menu'] == True
df_solicitantes2.loc[mask, 'solicita_menu'] = np.random.choice([True, False], mask.sum())
df_solicitantes2 = df_solicitantes2.sort_values(by='id_solicitante')
df_solicitantes2 = df_solicitantes2[['id_solicitante', 'id_viaje', 'solicita_menu']]


solicitudes_values = df_solicitantes2[['id_solicitante', 'id_viaje', 'solicita_menu']].values.tolist()
cur.executemany(
    "INSERT INTO solicitudes (id_solicitante, id_viaje, solicita_menu) VALUES (%s, %s, %s)",
    solicitudes_values
)

conn.commit()
conn.close()

conn = psycopg2.connect(
    dbname="project",
    user="project",
    password="project",
    host="postgres",
    port="5432"
)

cur = conn.cursor()

queries = [
"""CREATE TABLE query1 AS (
select d.id_solicitante, d.nombre, d.apellido, c.sexo, c.edad, c.trabajo, c.anyos_trabajados, c.movilidad, c.discapacidad, c.enfermedad,
f.familia_numerosa, f.edad_hijo, f.trabaja_hijo, h.hab_ind, p.renta, p.pension, p.tipo_pension, p.estado_civil, p.pension_conyuge, v.domicilio,
v.vehiculo, a.lista_espera, a.viaje_2021, a.viaje_2022, a.num_max_viaje_por_temp
from datos d, anyos_ant a, caract c, fam_num f, habitacion h, pensiones p, viajero v
where d.id_solicitante = a.id_solicitante and d.id_solicitante = c.id_solicitante and d.id_solicitante = f.id_solicitante 
and d.id_solicitante = h.id_solicitante and d.id_solicitante = p.id_solicitante  and d.id_solicitante = v.id_solicitante
);""",
    """CREATE TABLE query3 AS (
select v.id_viaje , v.id_destino, d.destino, d.tipo_destino,  v.id_precio, pr.duracion, pr.transporte, pr.sup_hab_ind, pr.precio, s.id_solicitante, m.mes, s.solicita_menu
from viajes v, destinos d, precios pr, solicitudes s, mes m 
where v.id_destino = d.id_destino and pr.id_precio = v.id_precio and s.id_viaje = v.id_viaje and m.id_viaje = v.id_viaje 
);""",
    """select q1.id_solicitante, q1.nombre, q1.apellido, q1.sexo, q1.edad, q1.trabajo, q1.anyos_trabajados, q1.movilidad, q1.discapacidad, q1.enfermedad,
q1.familia_numerosa, q1.edad_hijo, q1.trabaja_hijo, q1.hab_ind, q1.renta, q1.pension, q1.tipo_pension, q1.estado_civil, q1.pension_conyuge, q1.domicilio,
q1.vehiculo, q1.lista_espera, q1.viaje_2021, q1.viaje_2022, q1.num_max_viaje_por_temp, q3.id_viaje, q3.id_destino, q3.destino, q3.tipo_destino, q3.mes, q3.solicita_menu, q3.id_precio,
q3.duracion, q3.transporte, q3.sup_hab_ind, q3.precio
from query1 q1, query3 q3
where q1.id_solicitante = q3.id_solicitante;"""
]

for query in queries:
    cur.execute(query)

data = cur.fetchall()
columns = [desc[0] for desc in cur.description]
df = pd.DataFrame(data, columns=columns)

cur.close()
conn.close()

def asignacionPuntos(row):
    condiciones_edad = [
        (row['edad'] < 60),
        (row['edad'] == 60),
        ((61 < row['edad']) & (row['edad'] < 78)),
        (row['edad'] >= 78)
    ]

    scoresEdad = [1, 2,2+row['edad']-60, 20]
    score_edad = np.select(condiciones_edad, scoresEdad, default=0)
    
    condiciones_años_trab = [
        (row['anyos_trabajados'] < 20),
        (20 < row['anyos_trabajados']) & (row['anyos_trabajados'] < 25),
        ((26 < row['anyos_trabajados']) & (row['anyos_trabajados'] < 30)),
        (row['anyos_trabajados'] >= 30)
    ]

    scoresAños_trab=[10,20,30,40]
    score_años_trab=np.select(condiciones_años_trab,scoresAños_trab,default=0)

    condiciones_movilidad= [
        (row['movilidad']=='limitada'),
        (row['movilidad']=='media'),
        (row['movilidad']=='perfecta')
    ]
    scoresMovilidad=[10,20,30]
    score_movilidad=np.select(condiciones_movilidad,scoresMovilidad,default=0)
    
    condiciones_discapacidad=[
        (row['discapacidad']==False),
        (row['discapacidad']==True)
    ]
    scoresDiscapacidad=[0,25]
    score_discapacidad=np.select(condiciones_discapacidad,scoresDiscapacidad,default=0)

    condiciones_enfermedad=[
        (row['enfermedad']==False),
        (row['enfermedad']==True)
    ]
    scoresEnfermedad=[50,0]
    score_enfermedad=np.select(condiciones_enfermedad,scoresEnfermedad,default=0)

    condiciones_familia_numerosa=[
        (row['familia_numerosa']==False),#No es familia numerosa
        (row['familia_numerosa']==True) & (row['edad_hijo']<26) & (row['edad_hijo']>0) & (row['trabaja_hijo']==False), #familia numerosa con menor de 26 que no trabaja
        (row['familia_numerosa']==True) & (row['edad_hijo']<26) & (row['edad_hijo']>0) & (row['trabaja_hijo']==True), #familia numerosa con menor de 26 que trabaja
    ]

    scoresFamiliaNumerosa=[0,50,15]
    score_familia_numerosa=np.select(condiciones_familia_numerosa,scoresFamiliaNumerosa,default=0)

    condiciones_habitacion=[
        (row['hab_ind']==False), #Habitacion doble
        (row['hab_ind']==True) #habitacion individual
    ]

    scoresHabitacion=[20,0]
    score_habitacion_individual=np.select(condiciones_habitacion,scoresHabitacion,default=0)

    condiciones_renta=[
        (row['renta']<1),
        ((row['renta']<8500) & (row['renta']>1)),
        ((row['renta']<13000) & (row['renta']>8500)),
        ((row['renta']<16000) & (row['renta']>13000)),
        ((row['renta']<19000) & (row['renta']>16000)),
        ((row['renta']<22000) & (row['renta']>19000))
    ]
    scoresRenta=[50,40,30,20,10,0]
    score_renta=np.select(condiciones_renta,scoresRenta,default=0)

    condiciones_vehiculo=[
        (row['vehiculo']==False), #Habitacion doble
        (row['vehiculo']==True) #habitacion individual
    ]

    scores_vehiculo=[20,0]
    score_vehiculo_ind=np.select(condiciones_vehiculo,scores_vehiculo,default=0)
    
    condiciones_años_ant=[
        ((row['lista_espera']==True) & (row['viaje_2021']==True) & (row['viaje_2022']==True) & (row['num_max_viaje_por_temp']<2)),
        ((row['lista_espera']==True) & (row['viaje_2021']==False) & (row['viaje_2022']==False) & (row['num_max_viaje_por_temp']<2)),
        ((row['lista_espera']==True) & (row['viaje_2021']==False) & (row['viaje_2022']==True) & (row['num_max_viaje_por_temp']<2)),
        ((row['lista_espera']==True) & (row['viaje_2021']==True) & (row['viaje_2022']==False) & (row['num_max_viaje_por_temp']<2)),
        ((row['lista_espera']==True) & (row['viaje_2021']==True) & (row['viaje_2022']==True) & (row['num_max_viaje_por_temp']>1)),
        ((row['lista_espera']==True) & (row['viaje_2021']==False) & (row['viaje_2022']==True) & (row['num_max_viaje_por_temp']>1)),
        ((row['lista_espera']==True) & (row['viaje_2021']==True) & (row['viaje_2022']==False) & (row['num_max_viaje_por_temp']>1)),
        (row['lista_espera']==False)
    ]

    scores_años_ant=[40,70,50,60,5,10,15,0]
    score_años_ant=np.select(condiciones_años_ant,scores_años_ant,default=0)

    condiciones_destino=[
        (row['tipo_destino']=='circuitos_culturales'),
        (row['tipo_destino']=='turismo_naturaleza'),
        (row['tipo_destino']=='zona_baleares'),
        (row['tipo_destino']=='capitales_provincia'),
        (row['tipo_destino']=='zona_costera'),
        (row['tipo_destino']=='viaje_ceuta_melilla'),
        (row['tipo_destino']=='zona_canarias')
    ]

    scores_destinos=[50,35,20,0,10,70,30]
    score_destino=np.select(condiciones_destino,scores_destinos,default=0)

    condiciones_precio=[
        (row['id_precio']==1),
        (row['id_precio']==2),
        (row['id_precio']==3),
        (row['id_precio']==4),
        (row['id_precio']==5),
        (row['id_precio']==6),
        (row['id_precio']==7),
        (row['id_precio']==8),
        (row['id_precio']==9),
        (row['id_precio']==10),
        (row['id_precio']==11),
        (row['id_precio']==12),
        (row['id_precio']==13),
        (row['id_precio']==14),
        (row['id_precio']==15),
        (row['id_precio']==16),
        
    ]
    
    scores_precios=[12,11,13,5,8,9,14,3,2,10,15,1,4,7,16,6]
    score_precio=np.select(condiciones_precio,scores_precios,default=0)   

    condiciones_meses=[
        (row['mes']=='octubre'),
        (row['mes']=='noviembre'),
        (row['mes']=='diciembre'),
        (row['mes']=='enero'),
        (row['mes']=='febrero'),
        (row['mes']=='marzo'),
        (row['mes']=='abril'),
        (row['mes']=='mayo'),
        (row['mes']=='junio')
    ]
    
    scores_meses=[0,10,15,30,25,20,10,5,0]
    score_mes=np.select(condiciones_meses,scores_meses,default=0)  

    condiciones_menu=[
        (row['solicita_menu']==False), 
        (row['solicita_menu']==True)
    ]

    scores_menus=[0,20]
    score_menu=np.select(condiciones_menu,scores_menus,default=0)

    totalScore= score_edad + score_años_trab + score_movilidad + score_discapacidad + score_enfermedad + score_familia_numerosa + score_habitacion_individual + score_renta + score_vehiculo_ind + score_años_ant + score_destino + score_precio + score_mes + score_menu
    return totalScore

df['score_total'] = df.apply(asignacionPuntos, axis=1)

df_aux = df.copy()
df_aux['pension'] = np.where(df_aux['estado_civil'] == 'casado/a',
                             (df_aux['pension'] + df_aux['pension_conyuge']) / 1.33,
                             df_aux['pension'])

def asignacionPuntosPension(row):
    condiciones_pensiones=[
        ((row['pension']<13076) & (row['pension']>6786)),
        ((row['pension']<19365) & (row['pension']>13075)),
        ((row['pension']<25654) & (row['pension']>19364)),
        ((row['pension']<31943) & (row['pension']>25653)),
        (row['pension']>31942)
    ]
    scores_pension=[50,40,30,20,10]
    score_pension=np.select(condiciones_pensiones,scores_pension,default=0)
    return score_pension

df_aux['score_pension'] = df_aux.apply(asignacionPuntosPension, axis=1)
df_aux['score_total'] = df_aux['score_total'] + df_aux['score_pension']
df['score_total'] = df_aux['score_total']

selected_solicitantes = set()
for viaje in range(1, 5001):
    max_score_indices = df['id_viaje'] == viaje
    max_score_solicitante = df[max_score_indices].loc[df[max_score_indices]['score_total'].idxmax(), 'id_solicitante']
    
    if max_score_solicitante not in selected_solicitantes:
        selected_solicitantes.add(max_score_solicitante)
        restar_indices = (df['id_viaje'] != viaje) & (df['id_solicitante'] == max_score_solicitante)
        df.loc[restar_indices, 'score_total'] -= 300

selected_indices = df.groupby('id_viaje')['score_total'].idxmax()
df_selected = df.loc[selected_indices]
df_selected.to_json('/app/df_selected.json', orient='records')

print(f'Lo hemos conseguido!')
print(df_selected.head(20))

