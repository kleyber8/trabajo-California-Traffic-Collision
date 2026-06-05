import streamlit as st
from utils.database import (
    get_areas_severidad,
    get_raw_areas_sample,
    get_radar_factores_pre_pandemia,
    get_radar_factores_pandemia,
    get_waterfall_anual,
    get_raw_waterfall_sample,
    get_scatter_animado,
    get_raw_scatter_sample
)
from components.temporal_geografico_charts import (
    render_areas_severidad,
    render_radar_factores,
    render_waterfall_anual,
    render_scatter_animado
)

def mostrar_criticidad(fecha_ini, fecha_fin):
    st.markdown("""
    <div style="background-color: #121212; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 20px;">
        <h1 style="color: #D4AF37; margin: 0;">🕒 Criticidad Geográfica y Temporal</h1>
        <p style="color: #FFFFFF; font-size: 18px; margin-top: 5px;">
            <span style="color: #D4AF37; font-weight: bold;">Pre‑pandemia vs Pandemia</span> · 
            Evolución de accidentes y factores de riesgo (2018‑2021)
        </p>
        <p style="color: #CCCCCC; margin-bottom: 0;">Fuente: California Highway Patrol – SWITRS</p>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Cargando datos temporales..."):
        df_areas = get_areas_severidad(fecha_ini, fecha_fin)
        df_pre = get_radar_factores_pre_pandemia()
        df_pan = get_radar_factores_pandemia()
        df_waterfall = get_waterfall_anual(fecha_ini, fecha_fin)
        df_scatter = get_scatter_animado(fecha_ini, fecha_fin)

    total_entorno = df_areas['conteo'].sum() if not df_areas.empty else 0
    col1, col2, col3 = st.columns(3)
    col1.metric("Registros en entorno activo", f"{total_entorno:,}")
    col2.metric("Años analizados", "2018-2021")
    col3.metric("Total fatalidades", f"{df_scatter['killed_victims'].sum():,}" if not df_scatter.empty else "0")

    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Áreas de Severidad", "🕸️ Radar de Factores", "📉 Cascada Interanual", "🗺️ Mapa Animado"])

    with tab1:
        st.plotly_chart(render_areas_severidad(df_areas), use_container_width=True)
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.caption("Mostrando solamente 20 filas de colisiones (fecha y severidad).")
            df_raw = get_raw_areas_sample(fecha_ini, fecha_fin)
            st.dataframe(df_raw)

    with tab2:
        st.plotly_chart(render_radar_factores(df_pre, df_pan), use_container_width=True)
        st.caption("El gráfico radar muestra porcentajes agregados; no hay una tabla de datos subyacente con límite de 20 filas.")

    with tab3:
        st.plotly_chart(render_waterfall_anual(df_waterfall), use_container_width=True)
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.caption("Mostrando solamente 20 filas de colisiones (fechas).")
            df_raw = get_raw_waterfall_sample(fecha_ini, fecha_fin)
            st.dataframe(df_raw)

    with tab4:
        if not df_scatter.empty:
            st.plotly_chart(render_scatter_animado(df_scatter), use_container_width=True)
        else:
            st.warning("No hay datos para el mapa animado en este periodo.")
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.caption("Mostrando solamente 20 filas de accidentes fatales (ubicación, año, severidad).")
            df_raw = get_raw_scatter_sample(fecha_ini, fecha_fin)
            st.dataframe(df_raw)