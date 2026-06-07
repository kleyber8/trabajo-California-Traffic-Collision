import streamlit as st
from utils.database import ejecutar_consulta_limitada

def mostrar_consultas():
    st.markdown("""
    <div style="background-color: #121212; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 20px;">
        <h1 style="color: #D4AF37; margin: 0;">⛁ Querys: Preguntas del Profesor</h1>
        <p style="color: #FFFFFF; font-size: 18px; margin-top: 5px;">
            <span style="color: #D4AF37; font-weight: bold;">Consultas SQL avanzadas</span> · 
            Respuestas a los problemas planteados
        </p>
        <p style="color: #CCCCCC; margin-bottom: 0;">
            Fuente: <span style="color: #D4AF37;">California Highway Patrol</span> – SWITRS
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Pregunta 1", "Pregunta 2", "Pregunta 3", "Pregunta 4", "Pregunta 5"])

    with tab1:
        st.markdown("<h1 style='color: #D4AF37;'>⛁ Querys: Pregunta 1</h1>", unsafe_allow_html=True)
        st.divider()
        st.header("Pregunta 1")
        st.subheader("Conductores Reincidentes en Condiciones de Riesgo Compuesto")
        st.markdown("""**Enunciado:** Identifica los condados donde la proporción de accidentes que involucran simultáneamente presencia de alcohol, uso de teléfono celular y condiciones de iluminación deficiente supera en más de dos desviaciones estándar al promedio estatal de esa misma proporción.""")
        st.markdown("---")

        query_default_1 = """
WITH metricas_por_accidente AS (
    SELECT 
        c.location_type AS condado,
        CASE 
            WHEN (LOWER(p.party_sobriety) LIKE '%had been drinking%')
             AND (p.cellphone_in_use = '1')
             AND (LOWER(c.lighting) LIKE '%dark%' OR LOWER(c.lighting) LIKE '%dusk%' OR LOWER(c.lighting) LIKE '%dawn%')
            THEN 1 ELSE 0 
        END AS cumple_factores
    FROM collisions c
    JOIN parties p ON c.case_id = p.case_id
    WHERE c.location_type IS NOT NULL
),
estadisticas_condado AS (
    SELECT 
        condado,
        COUNT(*) AS total_accidentes,
        SUM(cumple_factores) AS accidentes_con_factores,
        AVG(cumple_factores) AS proporcion_condado
    FROM metricas_por_accidente
    GROUP BY condado
),
promedio_estatal AS (
    SELECT 
        AVG(proporcion_condado) AS media_estatal,
        STDDEV_SAMP(proporcion_condado) AS desv_estatal
    FROM estadisticas_condado
)
SELECT 
    e.condado,
    e.total_accidentes,
    e.accidentes_con_factores,
    ROUND(e.proporcion_condado, 5) AS proporcion,
    ROUND(p.media_estatal, 5) AS promedio_estatal,
    ROUND((e.proporcion_condado - p.media_estatal) / NULLIF(p.desv_estatal, 0), 2) AS desviaciones_estandar
FROM estadisticas_condado e, promedio_estatal p
WHERE (e.proporcion_condado - p.media_estatal) > (2 * p.desv_estatal)
ORDER BY desviaciones_estandar DESC
"""
        sql_input_1 = st.text_area("Escribe tu primera consulta:", value=query_default_1, height=200, key="sql_1_nueva")
        if st.button("Ejecutar primera Query", key="btn_1_nuevo"):
            try:
                resultado = ejecutar_consulta_limitada(sql_input_1, limite=20)
                st.dataframe(resultado, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

        st.divider()
        st.subheader("🔍 Prueba de validación (1 Desviación)")
        st.info("Umbral de 1 desviación estándar.")

        query_val_1 = """
WITH metricas_por_accidente AS (
    SELECT 
        c.location_type AS condado,
        CASE 
            WHEN (LOWER(p.party_sobriety) LIKE '%had been drinking%')
             AND (p.cellphone_in_use = '1')
             AND (LOWER(c.lighting) LIKE '%dark%' OR LOWER(c.lighting) LIKE '%dusk%' OR LOWER(c.lighting) LIKE '%dawn%')
            THEN 1 ELSE 0 
        END AS cumple_factores
    FROM collisions c
    JOIN parties p ON c.case_id = p.case_id
    WHERE c.location_type IS NOT NULL
),
estadisticas_condado AS (
    SELECT 
        condado,
        COUNT(*) AS total_accidentes,
        SUM(cumple_factores) AS accidentes_con_factores,
        AVG(cumple_factores) AS proporcion_condado
    FROM metricas_por_accidente
    GROUP BY condado
),
promedio_estatal AS (
    SELECT 
        AVG(proporcion_condado) AS media_estatal,
        STDDEV_SAMP(proporcion_condado) AS desv_estatal
    FROM estadisticas_condado
)
SELECT 
    e.condado,
    e.total_accidentes,
    e.accidentes_con_factores,
    ROUND(e.proporcion_condado, 5) AS proporcion,
    ROUND(p.media_estatal, 5) AS promedio_estatal,
    ROUND((e.proporcion_condado - p.media_estatal) / NULLIF(p.desv_estatal, 0), 2) AS desviaciones_estandar
FROM estadisticas_condado e, promedio_estatal p
WHERE (e.proporcion_condado - p.media_estatal) > (1 * p.desv_estatal)
ORDER BY desviaciones_estandar DESC
"""
        sql_val_1 = st.text_area("Consulta de Validación (1 DE):", value=query_val_1, height=200, key="sql_1_val_nueva")
        if st.button("Ejecutar Validación (1 DE)", key="btn_1_val_nuevo"):
            try:
                resultado_val = ejecutar_consulta_limitada(sql_val_1, limite=20)
                st.dataframe(resultado_val, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

    with tab2:
        st.markdown("<h1 style='color: #D4AF37;'>⛁ Querys: Pregunta 2</h1>", unsafe_allow_html=True)
        st.divider()
        st.header("Pregunta 2")
        st.subheader("Perfil de Víctimas Fatales según Franja Horaria y Tipo de Vía")
        st.markdown("""**Enunciado:** Construye un ranking de los 3 perfiles (franja horaria, rango etario y tipo de vía) con mayor cantidad de víctimas fatales para cada franja horaria.""")
        st.markdown("---")

        query_default_2 = """
WITH Pre_Analisis AS (
    SELECT 
        CASE 
            WHEN (CAST(SUBSTR(c.collision_time, 1, 2) AS INT) BETWEEN 0 AND 5) THEN '00-06 (Madrugada)'
            WHEN (CAST(SUBSTR(c.collision_time, 1, 2) AS INT) BETWEEN 6 AND 11) THEN '06-12 (Mañana)'
            WHEN (CAST(SUBSTR(c.collision_time, 1, 2) AS INT) BETWEEN 12 AND 17) THEN '12-18 (Tarde)'
            ELSE '18-24 (Noche)'
        END AS Franja_Horaria,
        CASE 
            WHEN v.victim_age < 18 THEN 'Menor <18'
            WHEN v.victim_age BETWEEN 18 AND 30 THEN '18-30'
            WHEN v.victim_age BETWEEN 31 AND 50 THEN '31-50'
            WHEN v.victim_age BETWEEN 51 AND 65 THEN '51-65'
            ELSE 'Mayor >65'
        END AS Rango_Etario,
        COALESCE(c.location_type, 'Vía Local/Calle') AS Tipo_Via,
        SUM(c.killed_victims) AS Cantidad_Fallecidos
    FROM collisions c
    INNER JOIN victims v ON c.case_id = v.case_id
    WHERE c.killed_victims > 0 AND v.victim_age IS NOT NULL
    GROUP BY 1, 2, 3
),
Calculo_Rankings AS (
    SELECT 
        Franja_Horaria,
        Rango_Etario,
        Tipo_Via,
        Cantidad_Fallecidos,
        SUM(Cantidad_Fallecidos) OVER (PARTITION BY Franja_Horaria) AS Total_Franja,
        DENSE_RANK() OVER (PARTITION BY Franja_Horaria ORDER BY Cantidad_Fallecidos DESC) AS Ranking
    FROM Pre_Analisis
)
SELECT 
    Franja_Horaria,
    Rango_Etario,
    Tipo_Via,
    Cantidad_Fallecidos,
    Total_Franja AS Total_Fallecidos_Franja,
    ROUND((CAST(Cantidad_Fallecidos AS FLOAT) / Total_Franja) * 100, 2) || '%' AS Porcentaje_Impacto
FROM Calculo_Rankings
WHERE Ranking <= 3
ORDER BY Franja_Horaria ASC, Cantidad_Fallecidos DESC
"""
        sql_input_2 = st.text_area("Escribe tu segunda consulta:", value=query_default_2, height=250, key="sql_2_nueva")
        if st.button("Ejecutar segunda Query", key="btn_2_nuevo"):
            try:
                resultado = ejecutar_consulta_limitada(sql_input_2, limite=20)
                st.dataframe(resultado, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

    with tab3:
        st.markdown("<h1 style='color: #D4AF37;'>⛁ Querys: Pregunta 3</h1>", unsafe_allow_html=True)
        st.divider()
        st.header("Pregunta 3")
        st.subheader("Evolución Mensual de la Severidad y Detección de Meses Atípicos")
        st.markdown("""**Enunciado:** Calcula mes a mes el índice de severidad e identifica meses con índice >30% sobre el promedio anual.""")
        st.markdown("---")

        query_default_3 = """
WITH metricas_mensuales AS (
    SELECT
        EXTRACT(YEAR FROM CAST(collision_date AS DATE)) AS anio,
        EXTRACT(MONTH FROM CAST(collision_date AS DATE)) AS mes,
        COUNT(*) AS total_accidentes_mes,
        (SUM(killed_victims * 3 + injured_victims * 1) / COUNT(*)) AS indice_mes
    FROM collisions
    WHERE collision_date IS NOT NULL
    GROUP BY anio, mes
),
promedio_anual AS (
    SELECT anio, AVG(indice_mes) AS promedio_anio
    FROM metricas_mensuales
    GROUP BY anio
)
SELECT
    m.anio,
    m.mes,
    ROUND(m.indice_mes, 4) AS indice_del_mes,
    ROUND(a.promedio_anio, 4) AS promedio_anual,
    ROUND(((m.indice_mes - a.promedio_anio) / a.promedio_anio) * 100, 2) AS variacion_porcentual
FROM metricas_mensuales m
JOIN promedio_anual a ON m.anio = a.anio
WHERE m.indice_mes > (a.promedio_anio * 1.30)
ORDER BY m.anio DESC, m.mes ASC
"""
        sql_input_3 = st.text_area("Escribe tu tercera consulta:", value=query_default_3, height=220, key="sql_3_nueva")
        if st.button("Ejecutar tercera Query", key="btn_3_nuevo"):
            try:
                resultado = ejecutar_consulta_limitada(sql_input_3, limite=20)
                st.dataframe(resultado, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

        st.divider()
        st.subheader("🔍 Prueba de validación (umbral de 5%)")
        st.info("Meses con índice superior al 5% sobre el promedio anual.")

        query_val_3 = """
WITH metricas_mensuales AS (
    SELECT
        EXTRACT(YEAR FROM CAST(collision_date AS DATE)) AS anio,
        EXTRACT(MONTH FROM CAST(collision_date AS DATE)) AS mes,
        COUNT(*) AS total_accidentes_mes,
        (SUM(killed_victims * 3 + injured_victims * 1) / COUNT(*)) AS indice_mes
    FROM collisions
    WHERE collision_date IS NOT NULL
    GROUP BY anio, mes
),
promedio_anual AS (
    SELECT anio, AVG(indice_mes) AS promedio_anio
    FROM metricas_mensuales
    GROUP BY anio
)
SELECT
    m.anio,
    m.mes,
    ROUND(m.indice_mes, 4) AS indice_del_mes,
    ROUND(a.promedio_anio, 4) AS promedio_anual,
    ROUND(((m.indice_mes - a.promedio_anio) / a.promedio_anio) * 100, 2) AS variacion_porcentual
FROM metricas_mensuales m
JOIN promedio_anual a ON m.anio = a.anio
WHERE m.indice_mes > (a.promedio_anio * 1.05)
ORDER BY m.anio DESC, m.mes ASC
"""
        sql_val_3 = st.text_area("Consulta de Validación (5%):", value=query_val_3, height=220, key="sql_3_val_nueva")
        if st.button("Ejecutar Validación (5%)", key="btn_3_val_nuevo"):
            try:
                resultado_val = ejecutar_consulta_limitada(sql_val_3, limite=20)
                st.dataframe(resultado_val, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

    with tab4:
        st.markdown("<h1 style='color: #D4AF37;'>⛁ Querys: Pregunta 4</h1>", unsafe_allow_html=True)
        st.divider()
        st.header("Pregunta 4")
        st.subheader("Rutas Estatales con Patrón de Reincidencia en el Mismo Tramo")
        st.markdown("""**Enunciado:** Detecta rutas con al menos 3 accidentes graves/fatales en un radio de 0.5 millas dentro del mismo año.""")
        st.markdown("---")

        query_default_4 = """
WITH accidentes AS (
    SELECT 
        case_id,
        location_type AS ruta,
        EXTRACT(YEAR FROM CAST(collision_date AS DATE)) AS anio,
        latitude,
        longitude,
        killed_victims,
        primary_collision_factor
    FROM collisions
    WHERE LOWER(collision_severity) IN ('fatal', 'pain')
      AND location_type IS NOT NULL
      AND latitude IS NOT NULL
      AND longitude IS NOT NULL
),
celdas AS (
    SELECT
        ruta,
        anio,
        ROUND(latitude, 2) AS lat_celda,
        ROUND(longitude, 2) AS lon_celda,
        COUNT(*) AS cantidad_accidentes,
        SUM(killed_victims) AS total_fatalidades,
        AVG(latitude) AS latitud_central,
        AVG(longitude) AS longitud_central
    FROM accidentes
    GROUP BY ruta, anio, lat_celda, lon_celda
    HAVING COUNT(*) >= 3
),
factor_moda AS (
    SELECT
        a.ruta,
        a.anio,
        ROUND(a.latitude,2) AS lat_celda,
        ROUND(a.longitude,2) AS lon_celda,
        a.primary_collision_factor,
        COUNT(*) AS freq,
        ROW_NUMBER() OVER (PARTITION BY a.ruta, a.anio, ROUND(a.latitude,2), ROUND(a.longitude,2) ORDER BY COUNT(*) DESC) AS rn
    FROM accidentes a
    JOIN celdas c ON a.ruta = c.ruta AND a.anio = c.anio 
                  AND ROUND(a.latitude,2) = c.lat_celda AND ROUND(a.longitude,2) = c.lon_celda
    GROUP BY a.ruta, a.anio, ROUND(a.latitude,2), ROUND(a.longitude,2), a.primary_collision_factor
)
SELECT
    c.ruta AS ruta_estatal,
    c.anio,
    c.latitud_central,
    c.longitud_central,
    c.cantidad_accidentes,
    c.total_fatalidades,
    f.primary_collision_factor AS factor_colision_mas_frecuente
FROM celdas c
LEFT JOIN factor_moda f ON c.ruta = f.ruta AND c.anio = f.anio 
                       AND c.lat_celda = f.lat_celda AND c.lon_celda = f.lon_celda AND f.rn = 1
ORDER BY c.cantidad_accidentes DESC
"""
        sql_input_4 = st.text_area("Escribe tu cuarta consulta:", value=query_default_4, height=280, key="sql_4_nueva")
        if st.button("Ejecutar cuarta Query", key="btn_4_nuevo"):
            try:
                resultado = ejecutar_consulta_limitada(sql_input_4, limite=20)
                st.dataframe(resultado, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

    
    with tab5:
        st.markdown("<h1 style='color: #D4AF37;'>⛁ Querys: Pregunta 5</h1>", unsafe_allow_html=True)
        st.divider()
        st.header("Pregunta 5")
        st.subheader("Comparativa de Comportamiento de Riesgo por Grupo Demográfico y Tendencia Temporal")
        st.markdown("""**Enunciado:** Construye un reporte que, para cada combinación de género y rango etario de los conductores declarados responsables del accidente (at_fault), muestre:
1) La tasa de accidentes con alcohol involucrado sobre el total de accidentes donde ese grupo fue responsable.
2) El ranking de esa tasa dentro de su mismo grupo de género.
3) La variación de esa tasa respecto al año inmediatamente anterior.
Incluye únicamente los grupos con más de 100 accidentes registrados como responsables y que muestren una tendencia creciente en al menos 2 años consecutivos.""")
        st.markdown("---")

        query_default_5 = """
WITH Datos_Base AS (
    SELECT 
        SUBSTR(c.collision_date, 1, 4) AS año,
        v.victim_sex AS genero,
        CASE 
            WHEN v.victim_age BETWEEN 18 AND 30 THEN '18-30'
            WHEN v.victim_age BETWEEN 31 AND 50 THEN '31-50'
            WHEN v.victim_age BETWEEN 51 AND 65 THEN '51-65'
            ELSE 'Otros'
        END AS rango_etario,
        CASE WHEN p.party_sobriety LIKE 'had been drinking%' THEN 1 ELSE 0 END AS con_alcohol
    FROM parties p
    JOIN collisions c ON p.case_id = c.case_id
    JOIN victims v ON p.case_id = v.case_id AND p.party_number = v.party_number
    WHERE v.victim_sex IN ('male', 'female')
),
Metricas_Anuales AS (
    SELECT 
        año, genero, rango_etario,
        COUNT(*) AS total_accidentes,
        SUM(con_alcohol) AS total_alcohol
    FROM Datos_Base
    GROUP BY año, genero, rango_etario
    HAVING total_accidentes > 100
),
Analisis_Tendencia AS (
    SELECT 
        *,
        ROUND((CAST(total_alcohol AS FLOAT) / total_accidentes) * 100, 2) AS tasa,
        LAG(ROUND((CAST(total_alcohol AS FLOAT) / total_accidentes) * 100, 2)) 
            OVER (PARTITION BY genero, rango_etario ORDER BY año) AS tasa_T1,
        LAG(ROUND((CAST(total_alcohol AS FLOAT) / total_accidentes) * 100, 2), 2) 
            OVER (PARTITION BY genero, rango_etario ORDER BY año) AS tasa_T2
    FROM Metricas_Anuales
)
SELECT 
    año,
    genero AS "Género",
    rango_etario AS "Rango Etario",
    tasa || '%' AS "Tasa Alcohol",
    ROUND(tasa - tasa_T1, 2) || '%' AS "Variación Anual",
    DENSE_RANK() OVER (PARTITION BY año, genero ORDER BY tasa DESC) AS "Rank_en_Género"
FROM Analisis_Tendencia
WHERE tasa > tasa_T1 AND tasa_T1 > tasa_T2
ORDER BY año DESC, tasa DESC
"""
        sql_input_5 = st.text_area("Escribe tu quinta consulta:", value=query_default_5, height=280, key="sql_5_final")
        if st.button("Ejecutar quinta Query", key="btn_5_final"):
            try:
                resultado = ejecutar_consulta_limitada(sql_input_5, limite=20)
                st.dataframe(resultado, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")