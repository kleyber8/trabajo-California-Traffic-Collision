import streamlit as st
import duckdb
import pandas as pd

# Conexión cacheada a MotherDuck (se abre una sola vez)
@st.cache_resource
def get_md_connection():
    token = st.secrets["motherduck"]["token"]
    return duckdb.connect(f'md:accidentes_california?motherduck_token={token}')

# Función de consulta con caché (10 minutos)
@st.cache_data(ttl=600)
def run_query(query):
    conn = get_md_connection()
    try:
        return conn.execute(query).df()
    except Exception as e:
        st.error(f"Error en consulta: {e}")
        return pd.DataFrame()

# Adaptación de obtener_datos: misma firma, misma funcionalidad
@st.cache_data
def obtener_datos(nombre_tabla, anio="Todos"):
    """
    Obtiene los datos de la tabla especificada desde MotherDuck.
    Soporta los nombres de tabla que ya usas en tu app:
    'collisions', 'parties', 'victims', 'case_ids' y aplica filtros WHERE directos
    """
    # Mapeo de nombres que usas en tu app a los nombres reales en MotherDuck
    mapeo_tablas = {
    "collisions": "collisions",
    "parties": "parties",
    "victims": "victims",
    "case_ids": "case_ids",
    # Si necesitas redirigir versiones lite a la tabla completa:
    "case_ids_lite": "case_ids",
    "collision_lite": "collisions",
    "parties_lite": "parties",
    "victims_lite": "victims",
    "involved_victims_part_0": "involved_victims"
    }
    tabla_real = mapeo_tablas.get(nombre_tabla, nombre_tabla)

# Construcción de query condicional eficiente
    condiciones = []
    
    # Filtrar por año en la base de datos si la tabla posee columnas temporales
    if anio != "Todos":
        if tabla_real == "collisions":
            # Extraer año de collision_date usando funciones nativas de DuckDB
            condiciones.append(f"YEAR(CAST(collision_date AS DATE)) = {anio}")
        # Si las tablas 'parties' o 'victims' no tienen fecha directa, se filtrarán posteriormente por cruce de case_id

    # Armar string de ejecución SQL
    if condiciones:
        query = f"SELECT * FROM {tabla_real} WHERE {' AND '.join(condiciones)}"
    else:
        query = f"SELECT * FROM {tabla_real}"

    df = run_query(query)

    if df.empty:
        st.warning(f"La tabla '{nombre_tabla}' no devolvió registros para los filtros seleccionados.")

    return df

@st.cache_data
def obtener_datos_procesados_con_cache():
    """
    Carga las tres tablas principales y realiza los cruces masivos (merges) 
    UNA sola vez. Almacena los DataFrames resultantes listos en la memoria RAM 
    para que compartan los mismos datos en todas las sesiones (tabs).
    """
    # Llamamos a las funciones que ya tienen caché de base de datos
    collisions = obtener_datos("collisions")
    parties = obtener_datos("parties")
    victims = obtener_datos("victims")
    
    if collisions.empty or parties.empty or victims.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # Realizar los merges pesados en memoria una única vez
    df_merged = collisions.merge(parties, on='case_id', how='left', suffixes=('', '_party'))
    
    df_victims_merged = victims.merge(
        collisions[['case_id', 'collision_severity', 'type_of_collision']], 
        on='case_id', 
        how='left'
    )
    
    # Extraemos límites de fechas globales para los controles deslizantes o inputs de app.py y sesiones
    collisions['collision_date'] = pd.to_datetime(collisions['collision_date'], errors='coerce')
    min_date = collisions['collision_date'].min()
    max_date = collisions['collision_date'].max()
    
    # Si las fechas son inválidas, ponemos valores seguros por defecto
    if pd.isnull(min_date): min_date = pd.to_datetime('2018-01-01')
    if pd.isnull(max_date): max_date = pd.to_datetime('2021-12-31')
    
    return df_merged, df_victims_merged, victims, min_date.date(), max_date.date()