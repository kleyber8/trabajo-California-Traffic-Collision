import streamlit as st
from utils.database import (
    get_severidad_vs_equipo,
    get_raw_severidad_equipo_sample,
    get_tendencia_alcohol_anual,
    get_raw_alcohol_sample,
    get_mapa_accidentes_fatales,
    get_raw_mapa_sample,
    get_boxplot_edad_tipo_colision,
    get_raw_boxplot_sample
)
from components.risk_factors_charts import (
    render_severidad_vs_equipo,
    render_tendencia_alcohol_anual,
    render_mapa_california,
    render_boxplot_edad_por_tipo_colision
)

def mostrar_factores_riesgo(fecha_ini, fecha_fin):
    st.markdown("""
    <div style="background-color: #121212; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 20px;">
        <h1 style="color: #D4AF37; margin: 0;">🚦 Factores de Riesgo en Colisiones</h1>
        <p style="color: #FFFFFF; font-size: 18px; margin-top: 5px;">
            <span style="color: #D4AF37; font-weight: bold;">Conductas, Equipamiento y Condiciones</span> · 
            Análisis del impacto en la severidad de los accidentes
        </p>
        <p style="color: #CCCCCC; margin-bottom: 0;">Fuente: California Highway Patrol – SWITRS</p>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Cargando datos de factores de riesgo..."):
        df_sev_equipo = get_severidad_vs_equipo(fecha_ini, fecha_fin)
        df_tendencia = get_tendencia_alcohol_anual(fecha_ini, fecha_fin)
        df_mapa = get_mapa_accidentes_fatales(fecha_ini, fecha_fin)
        df_boxplot = get_boxplot_edad_tipo_colision(fecha_ini, fecha_fin)

    total_acc = df_tendencia['conteo'].sum() if not df_tendencia.empty else 0
    total_vic = df_sev_equipo['conteo'].sum() if not df_sev_equipo.empty else 0
    fatalidades = df_mapa['killed_victims'].sum() if not df_mapa.empty else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Accidentes", f"{total_acc:,}")
    col2.metric("Total Víctimas", f"{total_vic:,}")
    col3.metric("Total Fatalidades", f"{int(fatalidades):,}")

    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Equipo de Seguridad", "📈 Tendencia Alcohol", "🗺️ Mapa de California", "📊 Edad vs Tipo Colisión"])

    with tab1:
        st.plotly_chart(render_severidad_vs_equipo(df_sev_equipo), use_container_width=True)
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.caption("Mostrando solamente 20 filas de víctimas (equipo y severidad).")
            df_raw = get_raw_severidad_equipo_sample(fecha_ini, fecha_fin)
            st.dataframe(df_raw)

    with tab2:
        st.plotly_chart(render_tendencia_alcohol_anual(df_tendencia), use_container_width=True)
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.caption("Mostrando solamente 20 filas de parties y collisions (fecha y sobriedad).")
            df_raw = get_raw_alcohol_sample(fecha_ini, fecha_fin)
            st.dataframe(df_raw)

    with tab3:
        if not df_mapa.empty:
            st.plotly_chart(render_mapa_california(df_mapa), use_container_width=True)
        else:
            st.warning("No hay datos con fatalidades en este periodo.")
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.caption("Mostrando solamente 20 filas de accidentes fatales (ubicación y severidad).")
            df_raw = get_raw_mapa_sample(fecha_ini, fecha_fin)
            st.dataframe(df_raw)

    with tab4:
        st.plotly_chart(render_boxplot_edad_por_tipo_colision(df_boxplot), use_container_width=True)
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.caption("Mostrando solamente 20 filas de víctimas (edad, tipo colisión, sexo).")
            df_raw = get_raw_boxplot_sample(fecha_ini, fecha_fin)
            st.dataframe(df_raw)