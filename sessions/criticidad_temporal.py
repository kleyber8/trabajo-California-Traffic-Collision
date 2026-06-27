import streamlit as st
import pandas as pd
from utils.database import (
    get_areas_severidad,
    get_raw_areas_sample,
    get_weather_lighting_data,
    get_road_lighting_data,
    get_tendencia_fatalidades
)
from components.temporal_geografico_charts import (
    render_areas_severidad,
    render_weather_lighting_grouped_bar,
    render_road_lighting_grouped_bar,
    render_road_lighting_bubble,
    render_tendencia_fatalidades
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
        df_weather_lighting = get_weather_lighting_data(fecha_ini, fecha_fin)
        df_road_lighting = get_road_lighting_data(fecha_ini, fecha_fin)
        df_tendencia = get_tendencia_fatalidades(fecha_ini, fecha_fin)

    total_entorno = df_areas['conteo'].sum() if not df_areas.empty else 0
    col1, col2, col3 = st.columns(3)
    col1.metric("Registros en entorno activo", f"{total_entorno:,}")
    col2.metric("Años analizados", "2018-2021")
    col3.metric("Total fatalidades", f"{df_tendencia['fatalidades'].sum():,}" if not df_tendencia.empty else "0")

    st.markdown("---")
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Áreas de Severidad",
        "🌤️ Clima e Iluminación",
        "🛣️ Superficie e Iluminación",
        "🫧 Burbujas: Superficie vs Iluminación",
        "📈 Tendencia de Fatalidades"
    ])

    # ------------------------- TAB 1: Áreas de severidad -------------------------
    with tab1:
        st.plotly_chart(render_areas_severidad(df_areas), use_container_width=True)

        st.markdown("""
**Interpretación del gráfico:**

Este gráfico de áreas muestra la evolución anual de los accidentes según su nivel de severidad entre 2018 y 2021. Se observa una tendencia general descendente en el número total de accidentes, con una caída particularmente pronunciada en 2020, que coincide con el inicio de la pandemia de COVID-19 y las medidas de confinamiento en California. Esta reducción afectó a todas las categorías de severidad, siendo más notoria en los casos de lesiones leves y solo daños materiales.

Sin embargo, en 2021 se produce un repunte significativo en todas las categorías, especialmente en los accidentes con solo daños materiales, lo que sugiere una recuperación gradual de la movilidad y la actividad vial. Es importante destacar que los accidentes fatales y con lesiones graves, aunque también disminuyeron durante la pandemia, mostraron una recuperación menos pronunciada, lo que podría indicar que, pese al aumento del tráfico, las medidas de seguridad y la reducción de la velocidad en zonas urbanas pudieron haber mitigado la gravedad de los siniestros.

Estos hallazgos reflejan cómo los factores externos, como las políticas de confinamiento y los cambios en los patrones de movilidad, impactan directamente en la siniestralidad vial, y subrayan la necesidad de mantener estrategias de prevención incluso en periodos de menor tráfico.
 """)
        
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.caption("Mostrando solamente 20 filas de colisiones (fecha y severidad).")
            df_raw = get_raw_areas_sample(fecha_ini, fecha_fin)
            st.dataframe(df_raw)

    


    # ------------------------- TAB 2: Clima e Iluminación (barras agrupadas) -------------------------
    with tab2:
        st.subheader("🌤️ Análisis: Condiciones Climáticas e Iluminación")
        if not df_weather_lighting.empty:
            weather_opts = sorted(df_weather_lighting['weather_1'].unique())
            lighting_opts = sorted(df_weather_lighting['lighting'].unique())
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                selected_weather = st.multiselect(
                    "Selecciona condiciones climáticas:",
                    weather_opts,
                    default=weather_opts,
                    key="weather_filter"
                )
            with col_f2:
                selected_lighting = st.multiselect(
                    "Selecciona condiciones de iluminación:",
                    lighting_opts,
                    default=lighting_opts,
                    key="lighting_filter"
                )
            df_filt = df_weather_lighting.copy()
            if selected_weather:
                df_filt = df_filt[df_filt['weather_1'].isin(selected_weather)]
            if selected_lighting:
                df_filt = df_filt[df_filt['lighting'].isin(selected_lighting)]
            if not df_filt.empty:
                fig = render_weather_lighting_grouped_bar(df_filt)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No hay datos con los filtros seleccionados.")
        else:
            st.warning("No hay datos de clima e iluminación para mostrar.")
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.dataframe(df_weather_lighting.head(20))

    # ------------------------- TAB 3: Superficie de la vía e Iluminación (barras agrupadas) -------------------------
    with tab3:
        st.subheader("🛣️ Análisis: Tipo de Superficie de la Vía e Iluminación (Barras Agrupadas)")
        if not df_road_lighting.empty:
            road_opts = sorted(df_road_lighting['road_surface'].unique())
            lighting_opts2 = sorted(df_road_lighting['lighting'].unique())
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                selected_road = st.multiselect(
                    "Selecciona tipo de superficie:",
                    road_opts,
                    default=road_opts,
                    key="road_filter"
                )
            with col_g2:
                selected_lighting2 = st.multiselect(
                    "Selecciona condiciones de iluminación:",
                    lighting_opts2,
                    default=lighting_opts2,
                    key="lighting_filter2"
                )
            df_filt = df_road_lighting.copy()
            if selected_road:
                df_filt = df_filt[df_filt['road_surface'].isin(selected_road)]
            if selected_lighting2:
                df_filt = df_filt[df_filt['lighting'].isin(selected_lighting2)]
            if not df_filt.empty:
                fig = render_road_lighting_grouped_bar(df_filt)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No hay datos con los filtros seleccionados.")
        else:
            st.warning("No hay datos de superficie e iluminación para mostrar.")

        st.markdown("""
**Interpretación del gráfico:**

Este gráfico de barras agrupadas permite comparar el número de accidentes según el tipo de superficie de la vía y las condiciones de iluminación. Se observa que la mayoría de los accidentes ocurren en superficies secas (dry), independientemente de la iluminación, lo que es esperable dado que esta condición es la más frecuente en California. Sin embargo, dentro de las superficies secas, los accidentes son significativamente más numerosos en condiciones de luz diurna (daylight) que en condiciones de oscuridad o penumbra.

Un hallazgo relevante es que, en superficies mojadas (wet) o resbaladizas (slippery), la proporción de accidentes nocturnos (dark with street lights) aumenta notablemente, lo que sugiere que la combinación de baja adherencia y mala visibilidad es especialmente peligrosa. Estos resultados refuerzan la necesidad de extremar las precauciones al conducir en condiciones climáticas adversas y de mantener una iluminación adecuada en las vías, especialmente en zonas de alto tránsito y durante la noche.

La categoría "Desconocido" (unknown) representa una proporción menor de casos, lo que indica una buena calidad del registro de datos.
""")
        
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.dataframe(df_road_lighting.head(20))

    # ------------------------- TAB 4: Gráfico de burbujas mejorado -------------------------
    with tab4:
        st.subheader("🫧 Relación entre Superficie de la Vía e Iluminación (Tamaño = Accidentes)")
        if not df_road_lighting.empty:
            road_opts_bubble = sorted(df_road_lighting['road_surface'].unique())
            lighting_opts_bubble = sorted(df_road_lighting['lighting'].unique())
            col_h1, col_h2 = st.columns(2)
            with col_h1:
                selected_road_bubble = st.multiselect(
                    "Filtrar por tipo de superficie:",
                    road_opts_bubble,
                    default=road_opts_bubble,
                    key="road_filter_bubble"
                )
            with col_h2:
                selected_lighting_bubble = st.multiselect(
                    "Filtrar por iluminación:",
                    lighting_opts_bubble,
                    default=lighting_opts_bubble,
                    key="lighting_filter_bubble"
                )
            df_filt_bubble = df_road_lighting.copy()
            if selected_road_bubble:
                df_filt_bubble = df_filt_bubble[df_filt_bubble['road_surface'].isin(selected_road_bubble)]
            if selected_lighting_bubble:
                df_filt_bubble = df_filt_bubble[df_filt_bubble['lighting'].isin(selected_lighting_bubble)]
            if not df_filt_bubble.empty:
                fig_bubble = render_road_lighting_bubble(df_filt_bubble)
                st.plotly_chart(fig_bubble, use_container_width=True)
            else:
                st.warning("No hay datos con los filtros seleccionados.")
        else:
            st.warning("No hay datos de superficie e iluminación para mostrar.")

        st.markdown("""
**Interpretación del gráfico de burbujas:**

Este gráfico de burbujas visualiza la relación entre el tipo de superficie de la vía, la condición de iluminación y el volumen de accidentes, donde el tamaño de cada burbuja representa la cantidad de siniestros. Se aprecia claramente que la combinación más crítica es la de "superficie seca con luz diurna" (dry + daylight), que concentra la mayor cantidad de accidentes, lo cual es consistente con la mayor exposición al tráfico durante el día.

Sin embargo, al analizar las proporciones relativas, se observa que las superficies mojadas (wet) o con nieve (snowy) presentan burbujas de tamaño considerable incluso en condiciones de oscuridad, lo que indica un riesgo elevado en estas condiciones. Esto es especialmente preocupante porque implica que, aunque el volumen total de accidentes en condiciones adversas es menor, la probabilidad de que ocurran en situaciones de baja visibilidad es alta.

Este análisis destaca la importancia de diseñar estrategias de seguridad vial diferenciadas según las condiciones de la vía y la iluminación, y sugiere que las campañas de prevención deberían enfatizar el riesgo en condiciones climáticas adversas, incluso cuando el tráfico es menor.
""")
        
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.dataframe(df_road_lighting.head(20))

    # ------------------------- TAB 5: Tendencia de fatalidades -------------------------
    with tab5:
        st.subheader("📈 Evolución de Fatalidades en el Tiempo")
        if not df_tendencia.empty:
            granularidad = st.radio("Agrupar por:", ["Mes", "Año"], horizontal=True, key="gran_tend")
            if granularidad == "Año":
                df_tendencia['año'] = pd.to_datetime(df_tendencia['mes']).dt.year
                df_line = df_tendencia.groupby('año')['fatalidades'].sum().reset_index()
                df_line.columns = ['fecha', 'fatalidades']
                df_line['fecha'] = df_line['fecha'].astype(str)
            else:
                df_line = df_tendencia.rename(columns={'mes': 'fecha'})
            fig = render_tendencia_fatalidades(df_line)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No hay datos de fatalidades en este periodo.")

        st.markdown("""
**Interpretación del gráfico:**

La evolución mensual de las fatalidades por accidentes de tránsito entre 2018 y 2021 muestra un patrón estacional con picos en los meses de verano y una caída notable a partir de marzo de 2020, coincidiendo con el inicio de la pandemia. El punto más bajo se registra en abril de 2020, con una reducción de aproximadamente el 40% respecto a los mismos meses de años anteriores, lo que evidencia el efecto de las restricciones de movilidad en la reducción de la mortalidad vial.

A partir de mediados de 2020 y durante todo 2021, se observa una recuperación gradual de las fatalidades, aunque sin alcanzar los niveles prepandemia. Esto sugiere que, si bien el tráfico se restableció, otros factores como el cambio en los hábitos de conducción, el mayor uso de modos de transporte alternativos o la implementación de medidas de seguridad vial pudieron haber contribuido a mantener las fatalidades por debajo de los niveles de 2018-2019.

Este comportamiento resalta la sensibilidad de la siniestralidad vial a factores externos y la importancia de monitorear tendencias para diseñar políticas de prevención adaptadas a contextos cambiantes.
""")
        
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.dataframe(df_tendencia.head(20))

    