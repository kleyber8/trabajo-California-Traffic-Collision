import streamlit as st
import duckdb
import pandas as pd

@st.cache_resource
def get_md_connection():
    token = st.secrets["motherduck"]["token"]
    return duckdb.connect(f'md:accidentes_california?motherduck_token={token}')

def ejecutar_consulta(sql: str, params=None):
    conn = get_md_connection()
    if params:
        return conn.execute(sql, params).df()
    return conn.execute(sql).df()

@st.cache_data(ttl=600)
def ejecutar_consulta_limitada(sql: str, params=None, limite=50):
    conn = get_md_connection()
    sql_limpia = sql.rstrip(';')
    if 'LIMIT' not in sql_limpia.upper():
        sql_limpia += f" LIMIT {limite}"
    if params:
        return conn.execute(sql_limpia, params).df()
    return conn.execute(sql_limpia).df()

# ------------------- DEMOGRAFÍA -------------------
def get_piramide_poblacional(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT 
        v.victim_sex,
        CASE 
            WHEN v.victim_age BETWEEN 0 AND 4 THEN '0-4'
            WHEN v.victim_age BETWEEN 5 AND 9 THEN '5-9'
            WHEN v.victim_age BETWEEN 10 AND 14 THEN '10-14'
            WHEN v.victim_age BETWEEN 15 AND 19 THEN '15-19'
            WHEN v.victim_age BETWEEN 20 AND 24 THEN '20-24'
            WHEN v.victim_age BETWEEN 25 AND 29 THEN '25-29'
            WHEN v.victim_age BETWEEN 30 AND 34 THEN '30-34'
            WHEN v.victim_age BETWEEN 35 AND 39 THEN '35-39'
            WHEN v.victim_age BETWEEN 40 AND 44 THEN '40-44'
            WHEN v.victim_age BETWEEN 45 AND 49 THEN '45-49'
            WHEN v.victim_age BETWEEN 50 AND 54 THEN '50-54'
            WHEN v.victim_age BETWEEN 55 AND 59 THEN '55-59'
            WHEN v.victim_age BETWEEN 60 AND 64 THEN '60-64'
            WHEN v.victim_age BETWEEN 65 AND 69 THEN '65-69'
            WHEN v.victim_age BETWEEN 70 AND 74 THEN '70-74'
            WHEN v.victim_age BETWEEN 75 AND 79 THEN '75-79'
            WHEN v.victim_age BETWEEN 80 AND 84 THEN '80-84'
            ELSE '85+'
        END AS rango_edad,
        COUNT(*) AS cantidad
    FROM victims v
    JOIN collisions c ON v.case_id = c.case_id
    WHERE v.victim_sex IN ('male', 'female')
      AND v.victim_age IS NOT NULL
      AND CAST(c.collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    GROUP BY v.victim_sex, rango_edad
    """
    return ejecutar_consulta(sql)

def get_raw_victims_sample(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT v.case_id, v.victim_age, v.victim_sex, v.victim_degree_of_injury
    FROM victims v
    JOIN collisions c ON v.case_id = c.case_id
    WHERE v.victim_sex IN ('male', 'female')
      AND v.victim_age IS NOT NULL
      AND CAST(c.collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    LIMIT 20
    """
    return ejecutar_consulta_limitada(sql, limite=20)

def get_distribucion_sexo(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT 
        CASE WHEN v.victim_sex = 'male' THEN 'Male' ELSE 'Female' END AS genero,
        COUNT(*) AS total
    FROM victims v
    JOIN collisions c ON v.case_id = c.case_id
    WHERE v.victim_sex IN ('male', 'female')
      AND CAST(c.collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    GROUP BY genero
    """
    return ejecutar_consulta(sql)

def get_edad_promedio_por_genero(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT 
        v.victim_sex AS genero,
        AVG(v.victim_age) AS edad_promedio
    FROM victims v
    JOIN collisions c ON v.case_id = c.case_id
    WHERE v.victim_sex IN ('male', 'female')
      AND v.victim_age IS NOT NULL
      AND CAST(c.collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    GROUP BY v.victim_sex
    """
    return ejecutar_consulta(sql)

# ------------------- FACTORES DE RIESGO -------------------
def get_severidad_vs_equipo(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT 
        v.victim_safety_equipment_1 AS equipo,
        v.victim_degree_of_injury AS severidad,
        COUNT(*) AS conteo
    FROM victims v
    JOIN collisions c ON v.case_id = c.case_id
    WHERE v.victim_safety_equipment_1 IS NOT NULL
      AND v.victim_degree_of_injury IS NOT NULL
      AND CAST(c.collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    GROUP BY equipo, severidad
    """
    return ejecutar_consulta(sql)

def get_raw_severidad_equipo_sample(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT v.victim_safety_equipment_1, v.victim_degree_of_injury
    FROM victims v
    JOIN collisions c ON v.case_id = c.case_id
    WHERE v.victim_safety_equipment_1 IS NOT NULL
      AND v.victim_degree_of_injury IS NOT NULL
      AND CAST(c.collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    LIMIT 20
    """
    return ejecutar_consulta_limitada(sql, limite=20)


def get_raw_alcohol_sample(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT c.collision_date, p.party_sobriety
    FROM parties p
    JOIN collisions c ON p.case_id = c.case_id
    WHERE CAST(c.collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    LIMIT 20
    """
    return ejecutar_consulta_limitada(sql, limite=20)

def get_fatalidades_por_condado_factor(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT 
        c.county_location AS condado,
        c.primary_collision_factor AS factor,
        SUM(c.killed_victims) AS fatalidades
    FROM collisions c
    WHERE c.killed_victims > 0
      AND c.county_location IS NOT NULL
      AND c.primary_collision_factor IS NOT NULL
      AND CAST(c.collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    GROUP BY condado, factor
    ORDER BY fatalidades DESC
    """
    return ejecutar_consulta(sql)

def get_boxplot_stats_edad_tipo_colision(fecha_ini: str, fecha_fin: str):
    sql = f"""
    WITH edades AS (
        SELECT 
            c.type_of_collision,
            v.victim_age
        FROM victims v
        JOIN collisions c ON v.case_id = c.case_id
        WHERE CAST(c.collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
          AND v.victim_age IS NOT NULL
          AND c.type_of_collision IS NOT NULL
    )
    SELECT 
        type_of_collision,
        MIN(victim_age) AS min,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY victim_age) AS q1,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY victim_age) AS median,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY victim_age) AS q3,
        MAX(victim_age) AS max
    FROM edades
    GROUP BY type_of_collision
    """
    return ejecutar_consulta(sql)

def get_total_fatalidades(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT SUM(killed_victims) AS total
    FROM collisions
    WHERE killed_victims > 0
      AND CAST(collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    """
    df = ejecutar_consulta(sql)
    return df.iloc[0]['total'] if not df.empty else 0

# ------------------- CRITICIDAD TEMPORAL -------------------
def get_areas_severidad(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT 
        EXTRACT(YEAR FROM CAST(collision_date AS DATE)) AS anio,
        CASE 
            WHEN LOWER(collision_severity) = 'fatal' THEN 'Fatal'
            WHEN LOWER(collision_severity) = 'pain' THEN 'Lesión Grave'
            WHEN LOWER(collision_severity) = 'other injury' THEN 'Lesión Leve'
            WHEN LOWER(collision_severity) = 'property damage only' THEN 'Solo Daños'
            ELSE 'Otro'
        END AS severidad,
        COUNT(*) AS conteo
    FROM collisions
    WHERE CAST(collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    GROUP BY anio, severidad
    ORDER BY anio
    """
    return ejecutar_consulta(sql)

def get_raw_areas_sample(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT collision_date, collision_severity
    FROM collisions
    WHERE CAST(collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    LIMIT 20
    """
    return ejecutar_consulta_limitada(sql, limite=20)

def get_radar_factores_pre_pandemia():
    sql = """
    SELECT 
        COUNT(CASE WHEN LOWER(party_sobriety) LIKE '%had been drinking%' THEN 1 END) * 100.0 / COUNT(*) AS alcohol,
        COUNT(CASE WHEN LOWER(party_sobriety) LIKE '%drug%' THEN 1 END) * 100.0 / COUNT(*) AS drogas,
        COUNT(CASE WHEN cellphone_in_use = '1' THEN 1 END) * 100.0 / COUNT(*) AS celular,
        COUNT(CASE WHEN LOWER(weather_1) LIKE '%rain%' OR LOWER(weather_1) LIKE '%snow%' OR LOWER(weather_1) LIKE '%fog%' THEN 1 END) * 100.0 / COUNT(*) AS clima_adverso,
        COUNT(CASE WHEN LOWER(lighting) LIKE '%dark%' OR LOWER(lighting) LIKE '%night%' THEN 1 END) * 100.0 / COUNT(*) AS oscuridad
    FROM parties p
    JOIN collisions c ON p.case_id = c.case_id
    WHERE CAST(c.collision_date AS DATE) < '2020-03-19'
    """
    return ejecutar_consulta(sql)

def get_radar_factores_pandemia():
    sql = """
    SELECT 
        COUNT(CASE WHEN LOWER(party_sobriety) LIKE '%had been drinking%' THEN 1 END) * 100.0 / COUNT(*) AS alcohol,
        COUNT(CASE WHEN LOWER(party_sobriety) LIKE '%drug%' THEN 1 END) * 100.0 / COUNT(*) AS drogas,
        COUNT(CASE WHEN cellphone_in_use = '1' THEN 1 END) * 100.0 / COUNT(*) AS celular,
        COUNT(CASE WHEN LOWER(weather_1) LIKE '%rain%' OR LOWER(weather_1) LIKE '%snow%' OR LOWER(weather_1) LIKE '%fog%' THEN 1 END) * 100.0 / COUNT(*) AS clima_adverso,
        COUNT(CASE WHEN LOWER(lighting) LIKE '%dark%' OR LOWER(lighting) LIKE '%night%' THEN 1 END) * 100.0 / COUNT(*) AS oscuridad
    FROM parties p
    JOIN collisions c ON p.case_id = c.case_id
    WHERE CAST(c.collision_date AS DATE) BETWEEN '2020-03-19' AND '2021-01-24'
    """
    return ejecutar_consulta(sql)

def get_waterfall_anual(fecha_ini: str, fecha_fin: str):
    sql = f"""
    WITH anual AS (
        SELECT 
            EXTRACT(YEAR FROM CAST(collision_date AS DATE)) AS anio,
            COUNT(*) AS total
        FROM collisions
        WHERE CAST(collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
        GROUP BY anio
        ORDER BY anio
    )
    SELECT 
        anio,
        total,
        LAG(total) OVER (ORDER BY anio) AS anio_anterior,
        total - COALESCE(LAG(total) OVER (ORDER BY anio), total) AS cambio
    FROM anual
    """
    return ejecutar_consulta(sql)

def get_raw_waterfall_sample(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT collision_date
    FROM collisions
    WHERE CAST(collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    LIMIT 20
    """
    return ejecutar_consulta_limitada(sql, limite=20)

def get_tendencia_fatalidades(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT 
        DATE_TRUNC('month', CAST(collision_date AS DATE)) AS mes,
        SUM(killed_victims) AS fatalidades
    FROM collisions
    WHERE killed_victims > 0
      AND CAST(collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    GROUP BY mes
    ORDER BY mes
    """
    return ejecutar_consulta(sql)

def get_global_date_range():
    sql = "SELECT MIN(CAST(collision_date AS DATE)) as min_date, MAX(CAST(collision_date AS DATE)) as max_date FROM collisions"
    df = ejecutar_consulta(sql)
    if not df.empty:
        return df.iloc[0]['min_date'], df.iloc[0]['max_date']
    return '2018-01-01', '2021-12-31'

def get_tendencia_alcohol_mensual(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT 
        DATE_TRUNC('month', CAST(c.collision_date AS DATE)) AS mes,
        CASE 
            WHEN LOWER(p.party_sobriety) LIKE '%had been drinking%' THEN 'Con Alcohol'
            WHEN LOWER(p.party_sobriety) LIKE '%had not been drinking%' THEN 'Sobrio'
            ELSE 'Otro/Desconocido'
        END AS condicion,
        COUNT(*) AS conteo
    FROM parties p
    JOIN collisions c ON p.case_id = c.case_id
    WHERE CAST(c.collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    GROUP BY mes, condicion
    ORDER BY mes
    """
    return ejecutar_consulta(sql)

def get_weather_lighting_data(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT 
        COALESCE(weather_1, 'Desconocido') AS weather_1,
        COALESCE(lighting, 'Desconocido') AS lighting,
        COUNT(*) AS conteo
    FROM collisions
    WHERE CAST(collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    GROUP BY weather_1, lighting
    ORDER BY weather_1, lighting
    """
    return ejecutar_consulta(sql)

def get_road_lighting_data(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT 
        COALESCE(road_surface, 'Desconocido') AS road_surface,
        COALESCE(lighting, 'Desconocido') AS lighting,
        COUNT(*) AS conteo
    FROM collisions
    WHERE CAST(collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
    GROUP BY road_surface, lighting
    ORDER BY road_surface, lighting
    """
    return ejecutar_consulta(sql)

def get_vehicle_type_severity(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT 
        p.statewide_vehicle_type AS tipo_vehiculo,
        c.collision_severity AS severidad,
        COUNT(*) AS conteo
    FROM parties p
    JOIN collisions c ON p.case_id = c.case_id
    WHERE CAST(c.collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
      AND p.statewide_vehicle_type IS NOT NULL
      AND c.collision_severity IS NOT NULL
    GROUP BY tipo_vehiculo, severidad
    ORDER BY tipo_vehiculo, conteo DESC
    """
    return ejecutar_consulta(sql)

def get_vehicle_year_severity(fecha_ini: str, fecha_fin: str):
    sql = f"""
    SELECT 
        p.vehicle_year,
        c.collision_severity AS severidad,
        COUNT(*) AS conteo
    FROM parties p
    JOIN collisions c ON p.case_id = c.case_id
    WHERE CAST(c.collision_date AS DATE) BETWEEN '{fecha_ini}' AND '{fecha_fin}'
      AND p.vehicle_year IS NOT NULL
      AND p.vehicle_year BETWEEN 1950 AND 2025  -- filtrar años extremos
      AND c.collision_severity IS NOT NULL
    GROUP BY vehicle_year, severidad
    ORDER BY vehicle_year
    """
    return ejecutar_consulta(sql)