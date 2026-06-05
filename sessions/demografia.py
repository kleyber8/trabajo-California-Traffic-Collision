import streamlit as st
from utils.database import (
    get_piramide_poblacional,
    get_distribucion_sexo,
    get_edad_promedio_por_genero,
    get_raw_victims_sample
)
from components.demographics_charts import render_piramide_poblacional, render_distribucion_sexo

def mostrar_demografia(fecha_ini, fecha_fin):
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

    with st.spinner("Consultando datos demográficos..."):
        df_piramide = get_piramide_poblacional(fecha_ini, fecha_fin)
        df_sexo = get_distribucion_sexo(fecha_ini, fecha_fin)
        df_edad_prom = get_edad_promedio_por_genero(fecha_ini, fecha_fin)

    if df_piramide.empty:
        st.warning("No hay datos para el periodo seleccionado.")
        return

    total_victimas = df_piramide['cantidad'].sum()
    masculino = df_piramide[df_piramide['victim_sex']=='male']['cantidad'].sum()
    pct_masc = (masculino / total_victimas * 100) if total_victimas else 0
    edad_promedio = df_edad_prom['edad_promedio'].mean() if not df_edad_prom.empty else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Víctimas", f"{total_victimas:,}")
    col2.metric("Edad Promedio", f"{edad_promedio:.1f} años")
    col3.metric("Hombres", f"{masculino:,} ({pct_masc:.1f}%)")

    st.markdown("---")
    col1, col2 = st.columns([2,1])
    with col1:
        st.plotly_chart(render_piramide_poblacional(df_piramide), use_container_width=True)
    with col2:
        st.plotly_chart(render_distribucion_sexo(df_sexo), use_container_width=True)

    with st.expander("📄 Ver datos utilizados en los gráficos (primeras 20 filas)"):
        st.caption("Mostrando solamente 20 filas de las víctimas consideradas.")
        df_raw = get_raw_victims_sample(fecha_ini, fecha_fin)
        st.dataframe(df_raw)