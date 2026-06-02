import streamlit as st
import pandas as pd
from utils.database import obtener_datos_procesados_con_cache
from components.demographics_charts import render_piramide_poblacional, render_distribucion_sexo

def mostrar_demografia(anio="Todos"):
    # Encabezado principal
    st.markdown("""
    <div style="background-color: #121212; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 20px;">
        <h1 style="color: #D4AF37; margin: 0;">🚦 Análisis de Colisiones de Tránsito en California</h1>
        <p style="color: #FFFFFF; font-size: 18px; margin-top: 5px;">
            <span style="color: #D4AF37; font-weight: bold;">SWITRS 2018–2021</span> · 
            Dashboard interactivo de datos geograficos de el estado de California
        </p>
        <p style="color: #CCCCCC; margin-bottom: 0;">
            Fuente: <span style="color: #D4AF37;">California Highway Patrol</span> – 
            Statewide Integrated Traffic Records System
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. CARGA ULTRA RÁPIDA: Traemos los datos cruzados y convertidos directos de RAM
    with st.spinner("Cargando datos demográficos optimizados..."):
        df_collisions, _, df_victims, min_date, max_date = obtener_datos_procesados_con_cache()

    if df_collisions.empty or df_victims.empty:
        st.error("No se pudieron cargar los datos. Verifica los archivos fuente en la carpeta 'data/'.")
        return
    
    df_victims_filtrado = df_victims.copy()
        
    # Estilo CSS para el slider (color dorado)
    st.markdown("""
    <style>
        /* Punto del slider (thumb) */
        div[data-baseweb="slider"] div[role="slider"] {
            background-color: #D4AF37 !important;
            border-color: #D4AF37 !important;
        }
        /* Valor encima del thumb */
        div[data-baseweb="slider"] div[data-testid="stThumbValue"] {
            color: #D4AF37 !important;
        }
        /* Barra de progreso */
        div[data-baseweb="slider"] > div > div {
            background-color: #D4AF37 !important;
        }
        /* Track completo */
        div[data-baseweb="slider"] div[data-testid="stTrack"] {
            background-color: #D4AF37 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Métricas resumen
    total_victimas = len(df_victims_filtrado)

    df_sex_clean = df_victims_filtrado[df_victims_filtrado['victim_sex'].isin(['male', 'female'])].copy()
    conteo_sexo = df_sex_clean['victim_sex'].value_counts()
    masculino = conteo_sexo.get('male', 0)
    femenino  = conteo_sexo.get('female', 0)
    total_sexo = masculino + femenino
    pct_masc = (masculino / total_sexo * 100) if total_sexo > 0 else 0

    edad_promedio = df_victims_filtrado['victim_age'].mean() if 'victim_age' in df_victims_filtrado.columns else 0.0

    col_met1, col_met2, col_met3 = st.columns(3)
    with col_met1:
        st.metric(label="Total de Víctimas", value=f"{total_victimas:,}")
    with col_met2:
        st.metric(label="Edad Promedio", value=f"{edad_promedio:.1f} años")
    with col_met3:
        st.metric(label="Hombres", value=f"{masculino:,} ({pct_masc:.1f}%)")

    st.markdown("---")

    # Gráficos
    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(render_piramide_poblacional(df_victims_filtrado), use_container_width=True)

    with col2:
        st.plotly_chart(render_distribucion_sexo(df_victims_filtrado), use_container_width=True)

    if fecha_inicio and fecha_fin:
        st.caption(f"📊 Datos del {fecha_inicio} al {fecha_fin} | Víctimas filtradas: {total_victimas:,}")