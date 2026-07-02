import streamlit as st
import pandas as pd
from utils.database import (
    get_severidad_vs_equipo,
    get_raw_severidad_equipo_sample,
    get_tendencia_alcohol_mensual,
    get_raw_alcohol_sample,
    get_boxplot_stats_edad_tipo_colision,
    get_total_fatalidades,
    get_fatalidades_por_condado_factor,
    get_vehicle_type_severity,
    get_vehicle_year_severity
)
from components.risk_factors_charts import (
    render_severidad_vs_equipo,
    render_tendencia_alcohol_mensual,
    render_boxplot_edad_por_tipo_colision,
    render_barras_fatalidades,
    render_vehicle_type_severity,
    render_vehicle_year_severity
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
        df_tendencia = get_tendencia_alcohol_mensual(fecha_ini, fecha_fin)
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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🛡️ Equipo de Seguridad",
        "📈 Tendencia Alcohol (Mensual)",
        "📊 Fatalidades por Condado/Factor",
        "📊 Edad vs Tipo Colisión",
        "🚗 Vehículo vs Severidad",
        "📅 Año del Vehículo vs Severidad"
    ])

    with tab1:
        if not df_sev_equipo.empty:
            equipos_disponibles = sorted(df_sev_equipo['equipo'].unique())
            selected_equipos = st.multiselect(
                "Selecciona los equipos de seguridad a mostrar:",
                equipos_disponibles,
                default=equipos_disponibles[:10] if len(equipos_disponibles) > 10 else equipos_disponibles,
                key="sel_equipos"
            )
            if selected_equipos:
                df_filt = df_sev_equipo[df_sev_equipo['equipo'].isin(selected_equipos)]
                st.plotly_chart(render_severidad_vs_equipo(df_filt), use_container_width=True)
            else:
                st.warning("Selecciona al menos un equipo.")
        else:
            st.warning("No hay datos para mostrar")
        st.markdown("""
**Interpretación del gráfico:**

Este gráfico de barras agrupadas muestra la relación entre el equipo de seguridad utilizado por las víctimas y la severidad de las lesiones sufridas. Se observa que el uso del cinturón de seguridad (lap belt used y shoulder harness used) está asociado con una mayor proporción de lesiones leves y una reducción significativa de casos fatales, en comparación con aquellos que no usaron ningún equipo o cuyo airbag no se desplegó.

Los casos fatales son más frecuentes en categorías como "air bag not deployed" y "lap/shoulder harness not used", lo que sugiere que la combinación de airbag y cinturón es crucial para la supervivencia en accidentes graves. Además, se aprecia que los motociclistas que no usan casco (driver, motorcycle helmet not used) presentan una proporción alarmantemente alta de lesiones graves y fatales, lo que refuerza la importancia de las campañas de uso obligatorio de casco.

Estos resultados evidencian que el equipo de seguridad es un factor determinante en la gravedad de las lesiones, y que las políticas de uso obligatorio de cinturón y casco deben mantenerse y reforzarse, especialmente en grupos de alto riesgo como los motociclistas y los ocupantes de vehículos sin sistemas de retención adecuados.
""")
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.dataframe(df_sev_equipo.head(20))

    with tab2:
        if not df_tendencia.empty:
            st.plotly_chart(render_tendencia_alcohol_mensual(df_tendencia), use_container_width=True)
        else:
            st.warning("No hay datos de tendencia de alcohol")
        st.markdown("""
**Interpretación del gráfico:**

Este gráfico de líneas muestra la evolución mensual de la cantidad de accidentes según la condición del conductor entre enero de 2018 y julio de 2021. Se observa que la categoría de conductores bajo la condición de "Sobrio" representa la mayor frecuencia absoluta de siniestralidad en la población, manteniéndose con fluctuaciones cíclicas estables en un rango de entre 50,000 y 70,000 accidentes mensuales.

Un aspecto destacable es el pronunciado descenso en la línea de conductores sobrios durante el primer semestre de 2020, alcanzando su punto mínimo histórico debido a las restricciones de movilidad por el confinamiento, para luego describir una tendencia de recuperación hacia su media habitual. Por otro lado, la categoría "Otro/Desconocido" muestra un comportamiento ligeramente ascendente en el tiempo, mientras que los accidentes registrados "Con Alcohol" se mantienen estables en el volumen más bajo de la muestra. Asimismo, la caída abrupta que se observa al cierre en julio de 2021 responde de manera típica a un sesgo por retraso en la consolidación de los datos (*reporting delay*).

Estos resultados evidencian que el comportamiento de la siniestralidad base responde fuertemente a factores externos de movilidad general. Desde una perspectiva estadística y actuarial, aunque la frecuencia de la categoría "Con Alcohol" sea la menor en volumen de eventos, este análisis descriptivo debe complementarse con el estudio de la severidad y el costo promedio de los siniestros para lograr una correcta evaluación y modelación del riesgo.
""")
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.dataframe(df_tendencia)

    with tab3:
        if not df_barras.empty:
            condados = sorted(df_barras['condado'].unique())
            selected_condados = st.multiselect(
                "Selecciona los condados a mostrar:",
                condados,
                default=condados[:5] if len(condados) > 5 else condados,
                key="sel_condados"
            )
            if selected_condados:
                df_filt = df_barras[df_barras['condado'].isin(selected_condados)]
                fig = render_barras_fatalidades(df_filt)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Selecciona al menos un condado.")
        else:
            st.warning("No hay datos de fatalidades en este periodo.")
        st.markdown("""
**Interpretación del gráfico:**

Este gráfico de barras agrupadas muestra la distribución de fatalidades por condado y factor de colisión. Se observa que los condados más poblados, como Alameda, Butte y Amador, concentran el mayor número de fatalidades, lo cual es consistente con su mayor densidad de tráfico y población. Sin embargo, al analizar los factores de colisión, se aprecia que las violaciones del código de vehículos (vehicle code violation) son el factor más frecuente en todos los condados, seguido de "other than driver" y "unknown".

Un hallazgo relevante es que en condados con menor volumen de fatalidades, como Del Norte, la proporción de fatalidades atribuidas a factores desconocidos o de "other improper driving" es relativamente mayor, lo que podría indicar una menor calidad en el registro de datos o una mayor incidencia de accidentes con causas no claramente identificadas.

Este análisis sugiere que las estrategias de prevención deben enfocarse en reducir las violaciones del código de vehículos, especialmente en los condados con mayor siniestralidad, y mejorar la calidad de los registros para identificar mejor las causas de los accidentes en zonas con menor densidad de tráfico.
""")
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.dataframe(df_barras.head(20))

    with tab4:
        if not df_boxplot_stats.empty:
            tipos = sorted(df_boxplot_stats['type_of_collision'].unique())
            max_tipos = 10
            selected_tipos = st.multiselect(
                "Selecciona los tipos de colisión a mostrar:",
                tipos,
                default=tipos[:min(len(tipos), max_tipos)],
                key="sel_tipos"
            )
            if len(selected_tipos) > max_tipos:
                st.warning(f"Has seleccionado más de {max_tipos} tipos. El gráfico puede verse amontonado. Reduce la selección.")
            if selected_tipos:
                df_filt = df_boxplot_stats[df_boxplot_stats['type_of_collision'].isin(selected_tipos)]
                st.plotly_chart(render_boxplot_edad_por_tipo_colision(df_filt), use_container_width=True)
            else:
                st.warning("Selecciona al menos un tipo de colisión.")
        else:
            st.warning("No hay datos suficientes para el boxplot.")
        st.markdown("""
**Interpretación del gráfico de cajas:**

El diagrama de cajas muestra la distribución de edades de las víctimas según el tipo de colisión. Se observa que los accidentes por alcance trasero (rear end) y colisiones laterales (broadside) afectan a un rango de edad más amplio, con edades que oscilan entre los 20 y los 60 años, lo que refleja el perfil típico de los conductores en activo. Por el contrario, los accidentes que involucran peatones (pedestrian) presentan una edad mediana más elevada y una mayor dispersión, lo que podría indicar una mayor vulnerabilidad de las personas mayores en este tipo de siniestros.

Los choques frontales (head-on) muestran la edad mediana más alta (alrededor de los 45 años) y una distribución más compacta, lo que sugiere que este tipo de colisiones afecta predominantemente a conductores de mediana edad. Este hallazgo es relevante para orientar campañas de seguridad vial específicas, por ejemplo, enfatizando la importancia del cinturón de seguridad y la conducción defensiva en grupos de edad con mayor riesgo.

En general, estos resultados confirman que el perfil etario de las víctimas varía significativamente según el tipo de colisión, lo que subraya la necesidad de diseñar políticas de prevención diferenciadas por grupo de edad y tipo de siniestro.
""")
        with st.expander("📄 Ver estadísticos utilizados (min, Q1, mediana, Q3, max)"):
            st.dataframe(df_boxplot_stats)

    with tab5:
        st.subheader("🚗 Comparación de Severidad por Tipo de Vehículo")
        df_vehicle_type = get_vehicle_type_severity(fecha_ini, fecha_fin)
        if not df_vehicle_type.empty:
            tipos_vehiculo = sorted(df_vehicle_type['tipo_vehiculo'].unique())
            selected_tipos = st.multiselect(
                "Selecciona los tipos de vehículo a comparar:",
                tipos_vehiculo,
                default=tipos_vehiculo[:5] if len(tipos_vehiculo) > 5 else tipos_vehiculo,
                key="sel_tipos_vehiculo"
            )
            if selected_tipos:
                df_filt = df_vehicle_type[df_vehicle_type['tipo_vehiculo'].isin(selected_tipos)]
                fig = render_vehicle_type_severity(df_filt)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Selecciona al menos un tipo de vehículo.")
        else:
            st.warning("No hay datos de tipos de vehículo para mostrar.")
        st.markdown("""
**Interpretación del gráfico:**

Este gráfico de barras agrupadas permite comparar la severidad de los accidentes según el tipo de vehículo involucrado. Se observa que los automóviles de pasajeros (passenger car) concentran la mayor cantidad de accidentes en todas las categorías de severidad, lo cual es consistente con su predominio en el parque automotor. Sin embargo, al analizar las proporciones relativas, se aprecia que las motocicletas (motorcycle or scooter) y los vehículos de construcción (highway construction) presentan una proporción significativamente mayor de accidentes fatales y con lesiones graves en comparación con los automóviles de pasajeros.

Los camiones (truck o truck trailer) también muestran una proporción elevada de accidentes con lesiones graves, posiblemente debido a su mayor tamaño y peso, que incrementan la energía del impacto. Por otro lado, los vehículos de emergencia (emergency vehicle) y las bicicletas (bicycle) presentan volúmenes menores, pero con una proporción alta de lesiones graves, lo que refleja su alta vulnerabilidad en el tránsito.

Estos hallazgos son clave para diseñar políticas de seguridad vial diferenciadas: campañas específicas para motociclistas y ciclistas, controles más estrictos para vehículos pesados, y mejoras en la infraestructura para proteger a los usuarios más vulnerables.
""")
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.dataframe(df_vehicle_type.head(20))

    with tab6:
        st.subheader("📅 Relación entre Año del Vehículo y Severidad")
        df_vehicle_year = get_vehicle_year_severity(fecha_ini, fecha_fin)
        if not df_vehicle_year.empty:
            fig = render_vehicle_year_severity(df_vehicle_year)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No hay datos de años de vehículo para mostrar.")
        st.markdown("""
**Interpretación del gráfico:**

Este gráfico de áreas muestra la evolución de los accidentes según el año de fabricación del vehículo y la severidad de las lesiones. Se observa que los vehículos más antiguos (anteriores a 1990) presentan una mayor proporción de accidentes fatales y con lesiones graves, mientras que los vehículos más recientes (a partir de 2010) muestran una mayor proporción de accidentes con solo daños materiales o lesiones leves. Esto sugiere que los avances en seguridad vehicular, como airbags, sistemas de frenado ABS y estructuras de absorción de impactos, han contribuido a reducir la gravedad de las lesiones en los accidentes.

Un hallazgo notable es el pico de accidentes en vehículos del año 2020, que coincide con el aumento del parque automotor y la recuperación post-pandemia. Sin embargo, la severidad en estos vehículos es menor que en los modelos más antiguos, lo que indica que, aunque el número de accidentes aumentó, la tecnología de seguridad ha mitigado su impacto.

Estos resultados subrayan la importancia de mantener actualizado el parque automotor y de fomentar el uso de vehículos con sistemas de seguridad avanzados, especialmente en grupos de alto riesgo como los conductores jóvenes y las flotas de transporte.
""")
        with st.expander("📄 Ver datos utilizados (primeras 20 filas)"):
            st.dataframe(df_vehicle_year.head(20))