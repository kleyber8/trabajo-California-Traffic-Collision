import streamlit as st
import pandas as pd
from utils.database import obtener_datos_procesados_con_cache
from components.temporal_geografico_charts import (
    render_areas_severidad,
    render_radar_factores,
    render_waterfall_anual,
    render_scatter_animado
)

def mostrar_criticidad(anio="Todos"):
    st.markdown("""
    <div style="background-color: #121212; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 20px;">
        <h1 style="color: #D4AF37; margin: 0;">🕒 Criticidad Geográfica y Temporal</h1>
        <p style="color: #FFFFFF; font-size: 18px; margin-top: 5px;">
            <span style="color: #D4AF37; font-weight: bold;">Pre‑pandemia vs Pandemia</span> · 
            Evolución de accidentes y factores de riesgo (2018‑2021)
        </p>
        <p style="color: #CCCCCC; margin-bottom: 0;">
            Fuente: <span style="color: #D4AF37;">California Highway Patrol</span> – SWITRS
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. OPTIMIZACIÓN DE CACHÉ: Traemos los datos cruzados y los límites de fechas directo de memoria
    with st.spinner("Cargando periodos temporales optimizados..."):
        df, _, _, min_date, max_date = obtener_datos_procesados_con_cache()

    if df.empty:
        st.error("No se pudieron cargar los datos necesarios.")
        return
    
    df['collision_date'] = pd.to_datetime(df['collision_date'], errors='coerce')
    
    with st.sidebar:
        st.markdown("### 📅 Definir periodos")
        
        # 1. Definir los valores deseados por defecto
        default_pre_start = pd.to_datetime('2018-01-01').date()
        default_pre_end   = pd.to_datetime('2019-12-31').date()
        default_pan_start = pd.to_datetime('2020-01-01').date()
        default_pan_end   = pd.to_datetime('2021-12-31').date()

        # 2. Controlar que no se salgan de los límites reales de la data (min_date y max_date)
        pre_start_val = max(min_date, min(default_pre_start, max_date))
        pre_end_val   = max(min_date, min(default_pre_end, max_date))
        pan_start_val = max(min_date, min(default_pan_start, max_date))
        pan_end_val   = max(min_date, min(default_pan_end, max_date))

        # 3. Renderizar los inputs con los valores protegidos
        pre_start = st.date_input("Pre‑pandemia inicio", value=pre_start_val,
                                  min_value=min_date, max_value=max_date)
        pre_end   = st.date_input("Pre‑pandemia fin",     value=pre_end_val,
                                  min_value=min_date, max_value=max_date)
        pan_start = st.date_input("Pandemia inicio",       value=pan_start_val,
                                  min_value=min_date, max_value=max_date)
        pan_end   = st.date_input("Pandemia fin",          value=pan_end_val,
                                  min_value=min_date, max_value=max_date)

    # DataFrames por periodo
    df_pre = df[(df['collision_date'] >= pd.to_datetime(pre_start)) & (df['collision_date'] <= pd.to_datetime(pre_end))]
    df_pan = df[(df['collision_date'] >= pd.to_datetime(pan_start)) & (df['collision_date'] <= pd.to_datetime(pan_end))]
    df_all = pd.concat([df_pre, df_pan])

    # Métricas rápidas
    col1, col2, col3 = st.columns(3)
    col1.metric("Pre‑pandemia", f"{len(df_pre):,}")
    col2.metric("Pandemia", f"{len(df_pan):,}")
    col3.metric("Variación", f"{len(df_pan) - len(df_pre):+,}")
    st.markdown("---")

    # Pestañas
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Áreas de Severidad",
        "🕸️ Radar de Factores",
        "📉 Cascada Interanual",
        "🗺️ Mapa Animado"
    ])

    with tab1:
        st.plotly_chart(render_areas_severidad(df_all), use_container_width=True)

    with tab2:
        st.plotly_chart(render_radar_factores(df_pre, df_pan), use_container_width=True)

    with tab3:
        st.plotly_chart(render_waterfall_anual(df_all), use_container_width=True)

    with tab4:
        st.plotly_chart(render_scatter_animado(df_all), use_container_width=True)