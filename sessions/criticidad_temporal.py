import streamlit as st
import pandas as pd
from utils.database import obtener_datos_procesados_con_cache
from components.temporal_geografico_charts import (
    render_areas_severidad,
    render_radar_factores,
    render_waterfall_anual,
    render_scatter_animado
)

def mostrar_criticidad(df_filtrado):
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
    
    if df_filtrado.empty:
        st.warning("No hay datos disponibles para el periodo seleccionado.")
        return

    # 2. OPTIMIZACIÓN DE CACHÉ: Traemos los datos cruzados y los límites de fechas directo de memoria
    with st.spinner("Cargando periodos temporales optimizados..."):
        df_master, _, _, min_date, max_date = obtener_datos_procesados_con_cache()

    if df_master.empty:
        st.error("No se pudieron cargar los datos necesarios.")
        return
    
    df_master['collision_date'] = pd.to_datetime(df_master['collision_date'], errors='coerce')
    
    # Segmentación fija para gráficos comparativos (ej. Radar) sin inputs en la UI
    fecha_limite_pandemia_inicio = pd.to_datetime('2020-03-19')
    fecha_limite_pandemia_fin    = pd.to_datetime('2021-01-24')

    # DataFrames de control para comparativas internas
    df_pre = df_master[df_master['collision_date'] < fecha_limite_pandemia_inicio]
    df_pan = df_master[(df_master['collision_date'] >= fecha_limite_pandemia_inicio) & 
                       (df_master['collision_date'] <= fecha_limite_pandemia_fin)]
    
# Métricas dinámicas superiores basadas en el entorno activo seleccionado en la app
    total_entorno_activo = len(df_filtrado)
    total_historico_base = len(df_master)
    representacion_pct = (total_entorno_activo / total_historico_base * 100) if total_historico_base > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Registros en Entorno Activo", f"{total_entorno_activo:,}")
    col2.metric("Registros totales de la data", f"{total_historico_base:,}")
    col3.metric("Proporción", f"{representacion_pct:.1f}%")
    st.markdown("---")

    # Pestañas
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Áreas de Severidad",
        "🕸️ Radar de Factores",
        "📉 Cascada Interanual",
        "🗺️ Mapa Animado"
    ])

    with tab1:
        st.plotly_chart(render_areas_severidad(df_filtrado), use_container_width=True)

    with tab2:
        st.plotly_chart(render_radar_factores(df_pre, df_pan), use_container_width=True)

    with tab3:
        st.plotly_chart(render_waterfall_anual(df_filtrado), use_container_width=True)

    with tab4:
        st.plotly_chart(render_scatter_animado(df_filtrado), use_container_width=True)