import streamlit as st
import pandas as pd
from utils.database import (
    get_severidad_vs_equipo,
    get_raw_severidad_equipo_sample,
    get_tendencia_alcohol_mensual,
    get_raw_alcohol_sample,
    get_boxplot_stats_edad_tipo_colision,
    get_total_fatalidades,
    get_fatalidades_por_condado_factor
)
from components.risk_factors_charts import (
    render_severidad_vs_equipo,
    render_tendencia_alcohol_mensual,
    render_boxplot_edad_por_tipo_colision,
    render_barras_fatalidades
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
        df_tendencia = get_tendencia_alcohol_mensual(fecha_ini, fecha_fin)   # nueva función mensual
        df_boxplot_stats = get_boxplot_stats_edad_tipo_colision(fecha_ini, fecha_fin)
        total_fatalidades = get_total_fatalidades(fecha_ini, fecha_fin)
        df_barras = get_fatalidades_por_condado_factor(fecha_ini, fecha_fin)

    total_acc = df_tendencia['conteo'].sum() if not df_tendencia.empty else 0
    total_vic = df_sev_equipo['conteo'].sum() if not df_sev_equipo.empty else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Accidentes", f"{total_acc:,}")
    col2.metric("Total Víctimas", f"{total_vic:,}")
    col3.metric("Total Fatalidades", f"{int(total_fatalidades):,}")

    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Equipo de Seguridad", "📈 Tendencia Alcohol", "📊 Fatalidades por Condado/Factor", "📊 Edad vs Tipo Colisión"])

    # ---------- TAB 1: Equipo de Seguridad ----------
    with tab1:
        # Filtro de top N equipos para que el eje X no se sature
        equipos = df_sev_equipo.groupby('equipo')['conteo'].sum().nlargest(15).index.tolist()
        top_n = st.slider("Mostrar top N equipos de seguridad:", 5, 20, 10, key="top_equipos")
        equipos_top = df_sev_equipo.groupby('equipo')['conteo'].sum().nlargest(top_n).index
        df_filtrado = df_sev_equipo[df_sev_equipo['equipo'].isin(equipos_top)]
        st.plotly_chart(render_severidad_vs_equipo(df_filtrado), use_container_width=True)
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            df_raw = get_raw_severidad_equipo_sample(fecha_ini, fecha_fin)
            st.dataframe(df_raw)

    # ---------- TAB 2: Tendencia Alcohol (mensual) ----------
    with tab2:
        st.plotly_chart(render_tendencia_alcohol_mensual(df_tendencia), use_container_width=True)
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            df_raw = get_raw_alcohol_sample(fecha_ini, fecha_fin)
            st.dataframe(df_raw)

    # ---------- TAB 3: Fatalidades por Condado/Factor (barras agrupadas) ----------
    with tab3:
        if not df_barras.empty:
            # Filtro: top N condados
            top_n_cond = st.slider("Mostrar top N condados con más fatalidades:", 5, 30, 10, key="top_condados")
            condados_top = df_barras.groupby('condado')['fatalidades'].sum().nlargest(top_n_cond).index
            df_filt = df_barras[df_barras['condado'].isin(condados_top)]
            fig = render_barras_fatalidades(df_filt)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No hay datos de fatalidades en este periodo.")
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.dataframe(df_barras.head(20))

    # ---------- TAB 4: Boxplot (con selector de tipos de colisión) ----------
    with tab4:
        if not df_boxplot_stats.empty:
            tipos = sorted(df_boxplot_stats['type_of_collision'].unique())
            selected_tipos = st.multiselect("Selecciona tipos de colisión a mostrar:", tipos, default=tipos[:5] if len(tipos) > 5 else tipos, key="box_tipos")
            df_filt_stats = df_boxplot_stats[df_boxplot_stats['type_of_collision'].isin(selected_tipos)]
            if not df_filt_stats.empty:
                st.plotly_chart(render_boxplot_edad_por_tipo_colision(df_filt_stats), use_container_width=True)
            else:
                st.warning("No hay datos para los tipos seleccionados.")
        else:
            st.warning("No hay datos suficientes para el boxplot.")
        with st.expander("📄 Ver estadísticos utilizados (min, Q1, mediana, Q3, max)"):
            st.dataframe(df_boxplot_stats)