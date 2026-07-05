import streamlit as st

def mostrar_conclusiones():
    # 1. Banner Superior (Indentado dentro de la función)
    st.markdown("""
    <div style="background-color: #121212; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 20px;">
        <h1 style="color: #D4AF37; margin: 0;">Conclusiones: Proyecto SWITRS</h1>
        <p style="color: #FFFFFF; font-size: 18px; margin-top: 5px;">
            <span style="color: #D4AF37; font-weight: bold;">Conclusiones y Recomendaciones Finales</span>
        </p>
        <p style="color: #CCCCCC; margin-bottom: 0;">
            Fuente: <span style="color: #D4AF37;">California Highway Patrol</span> – SWITRS
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # 2. Estilos CSS personalizados (Modificados a tonos Dorados)
    st.markdown("""
        <style>
        .main-title {
            font-size: 38px !important;
            font-weight: 700;
            color: #D4AF37; /* Dorado Principal */
            margin-bottom: 5px;
        }
        .subtitle {
            font-size: 18px !important;
            color: #4B5563;
            margin-bottom: 30px;
            font-style: italic;
        }
        .section-title {
            font-size: 24px !important;
            font-weight: 600;
            color: #D4AF37; /* Dorado para Títulos de Sección */
            border-bottom: 2px solid #E5E7EB;
            padding-bottom: 8px;
            margin-top: 25px;
            margin-bottom: 15px;
        }
        .subsection-title {
            font-size: 19px !important;
            font-weight: 600;
            color: #F3CD5F; /* Dorado más claro para Subtítulos */
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .custom-body {
            font-size: 16px !important;
            line-height: 1.6 !important;
            text-align: justify;
        }
        </style>
    """, unsafe_allow_html=True)

   # 3. Introducción / Resumen Ejecutivo 
    st.markdown("""
    <div style="background-color: #1a1a1a; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 20px; border-top: 1px solid #2d2d2d; border-right: 1px solid #2d2d2d; border-bottom: 1px solid #2d2d2d;">
        <p class="custom-body" style="color: #E0E0E0; margin: 0;">
            El análisis de los datos de siniestralidad vial en el estado de California entre 2018 y 2021, 
            extraídos del sistema de SWITRS, ha permitido extraer millones de filas de datos crudos en 
            información de valor. A través de un enfoque documental y descriptivo, este proyecto se propuso 
            responder a la pregunta de investigación sobre cómo identificar los perfiles de vulnerabilidad de 
            las víctimas y el impacto de los factores de riesgo tanto ambientales como los de conducta de los 
            usuarios peatones y conductores. Se integraron herramientas como Streamlit y Power BI para lograr 
            obtener una mejor perspectiva de la interacción humana, temporal y del entorno con la seguridad vial.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown('<p class="section-title">DESARROLLO Y HALLAZGOS DEL ESTUDIO</p>', unsafe_allow_html=True)

    # 4. Configuración de Pestañas (Tabs)
    tab1, tab2, tab3 = st.tabs([
        "1. Perfil Demográfico", 
        "2. Factores de Riesgo", 
        "3. Dinámica Temporal"
    ])

    with tab1:
        st.markdown('<p class="subsection-title">Perfil Demográfico y Grupos de Alta Vulnerabilidad</p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="custom-body">
        Dando respuesta al primer objetivo específico, los datos demográficos revelan un sesgo de género 
        y edad crítico: los hombres jóvenes y adultos (entre 15 y 44 años) concentran la mayor cantidad de 
        víctimas. Este comportamiento sumando la edad mediana de 35.3 años confirma que las colisiones 
        impactan mayormente a la población económicamente activa.
        <br><br>
        La probabilidad de sufrir un atropello fatal o grave en calidad de peatón aumenta drásticamente en 
        la vejez, esto se ve además, en la progresiva reducción de registros a partir de los 65 años, que 
        muestra una menor exposición al tránsito, siendo estos más involucrados como siniestros de peatones.
        </p>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown('<p class="subsection-title">Factores de Riesgo, Ambientales y Conductuales</p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="custom-body">
        El estudio determinó de manera cuantitativa el peso que poseen las decisiones humanas en la severidad 
        de las lesiones. Al evaluar la efectividad del equipamiento de protección, se comprobó que el uso del 
        cinturón de seguridad se correlaciona con los siniestros que solo resultan en lesiones leves y 
        disminuyen los desenlaces fatales. En contraste, la tasa de mortalidad se dispara en registros donde 
        la bolsa de aire no se despegó o no usaron el cinturón de seguridad, confirmando de manera estadística 
        que usar sistemas de seguridad es indispensable para la supervivencia. En usuarios motociclistas y 
        bicicletas que omiten el uso de casco sufren una proporción alta de afectaciones graves y muertes. 
        <br><br>
        A nivel geográfico, las violaciones al código de vehículos sobresalen como la causa primaria y más 
        frecuente de fatalidad con una concentración en los condados de mayor densidad de población y tráfico, 
        tales como Alameda, Butte y Amador. En contraparte, zonas de menor densidad, como el condado de Del Norte, 
        muestran una proporción inusualmente alta de causas registradas como "desconocidas".
        <br><br>
        El análisis de la superficie de la vía y la iluminación arrojó que la mayor densidad de tráfico se da en 
        ambientes secos y con iluminación del día, pero no explica realmente la peligrosidad del entorno. Esta 
        verdadera criticidad se observa en superficies mojadas o con nieve, sobre todo en lugares con mala 
        iluminación pública. Esto demuestra que la combinación de baja adherencia y visibilidad altera los 
        patrones de conducción, elevando el riesgo y demostrando que las infraestructuras de iluminación actuales 
        son insuficientes cuando el clima empeora.
        <br><br>
        Por último, es importante denotar que los vehículos fabricados antes de 1990 muestran una marca superior de 
        desenlaces fatales y lesiones críticas ante un siniestro. En sentido inverso, los modelos producidos a partir 
        del año 2010 muestran lesiones leves o daños materiales en su mayoría. Esto demuestra que innovaciones como 
        las estructuras con zonas de deformación programada, los frenos ABS y los airbags múltiples han sido 
        altamente eficientes en mitigar el daño físico real de los usuarios.
        </p>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown('<p class="subsection-title">Dinámica Temporal: Pre-pandemia, Pandemia y el Reto de la Recuperación</p>', unsafe_allow_html=True)
        
        with st.expander("Periodo Pre-pandemia (2018-2019)", expanded=True):
            st.markdown('<p class="custom-body">Se caracterizó por volúmenes de accidentes e índices de mortalidad vial elevados pero estables, reflejando el comportamiento normal de la movilidad en California.</p>', unsafe_allow_html=True)
            
        with st.expander("Periodo de Pandemia (2020)", expanded=True):
            st.markdown('<p class="custom-body">Se registró una caída drástica de la siniestralidad, alcanzando su punto más bajo en abril de 2020 con una reducción cercana al 40% en las fatalidades debido a los confinamientos estrictos. No obstante, la reducción drástica de vehículos en circulación generó autopistas despejadas que propiciaron un incremento en los excesos de velocidad, manteniendo índices de severidad elevados a pesar del descenso en el tráfico masivo.</p>', unsafe_allow_html=True)
            
        with st.expander("Periodo Post-pandemia (2021)", expanded=True):
            st.markdown('<p class="custom-body">Los datos reflejan un repunte significativo en la cantidad de accidentes, impulsado principalmente por siniestros de solo daños materiales, marcando el retorno a la movilidad presencial. Pese a este incremento, las fatalidades y las lesiones severas no se recuperaron a la misma velocidad ni alcanzaron los picos del periodo 2018-2019.</p>', unsafe_allow_html=True)

    st.divider()

    # 5. Sección de Conclusión General
    st.markdown('<p class="section-title">Conclusión General</p>', unsafe_allow_html=True)
    st.markdown("""
    <p class="custom-body">
    En conclusión, el presente estudio proporciona evidencia científica concluyente de que la siniestralidad 
    vial no constituye un evento fortuito o de casualidad, sino un proceso de patrones espaciales, temporales 
    y humanos predecibles. Al resolver la pregunta de investigación planteada, se demostró que un análisis 
    exploratorio visual avanzado es capaz de dar con las razones de riesgo. Los factores demográficos personales 
    (como el género masculino y el rango de edad productiva) interactúan de forma estrecha con variables 
    situacionales (vías mojadas durante la noche) y fallas conductuales (violaciones normativas o desuso de 
    cinturón y casco) para expresar el grado de gravedad y la probabilidad de supervivencia en un siniestro.
    <br><br>
    Este proyecto de nivel estadístico universitario puede ser un modelo 
    operativo útil que certifica cómo los datos abiertos pueden ser depurados y 
    estructurados para guiar al desarrollo de auditorías viales oportunas e intervenciones de seguridad vial.
    </p>
    """, unsafe_allow_html=True)

    st.divider()

    # 6. Sección de Recomendaciones Finales
    st.markdown('<p class="section-title">Recomendaciones Finales para la Seguridad Vial (California y el Mundo)</p>', unsafe_allow_html=True)
    st.markdown('<p class="custom-body">Derivado de los hallazgos reales del análisis de datos de SWITRS, se estructuran las siguientes recomendaciones, aplicables tanto en el contexto del estado de California como a nivel global:</p><br>', unsafe_allow_html=True)

    recoms = [
        ("Campañas de Concienciación segmentada", "Recomendar el abandono de publicidad vial genérica. Los programas de concientización sobre velocidad, respeto al código de tránsito y uso de elementos de seguridad deben enfocarse en el perfil demográfico identificado: hombres de 15 a 44 años. Las publicidades deben pautarse en canales de alto consumo para este segmento."),
        ("Auditorías de Infraestructura Lumínica en Pavimentos Críticos", "Implementar programas de ingeniería urbana dirigidos a mejorar luminarias y aplicar asfaltos de alta porosidad (drenantes) en los tramos viales donde el cruce de variables 'superficie mojada / clima adverso + nocturnidad' demostró concentrar reportes críticos de siniestralidad."),
        ("Rediseño Urbano Enfocado en la Vulnerabilidad del Peatón Mayor", "Desarrollar intervenciones de infraestructura en zonas con alta población de la tercera edad. Extender los tiempos de cruce en semáforos peatonales, construir islas de refugio en avenidas de múltiples carriles e implementar señalización podotáctil y reflectiva avanzada en intersecciones."),
        ("Planes de seguridad ante rutas despejadas", "Ante reducciones de flujos vehiculares como se vio en 2020-2021, las autoridades deben activar de inmediato reducciones temporales en los límites de velocidad permitidos y reforzar el patrullaje automatizado (radares); esto evitará que la disminución de la congestión de autos incite a los conductores al exceso de velocidad en rutas despejadas."),
        ("Políticas de Renovación", "Impulsar normativas o publicidad que incentive la sustitución de vehículos con más de veinte años de antigüedad o que carezcan de sistemas de retención modernos."),
        ("Democratización Actuarial del Dato Vial", "Sugerir a las administraciones públicas y cuerpos policiales del mundo la migración de sus sistemas de registro hacia plataformas interactivas en tiempo real. El uso tradicional de reportes estáticos en formato PDF o excel entorpece la capacidad de reacción; la visualización dinámica orientada a la toma de decisiones permite a planificadores urbanos, compañías y autoridades policiales localizar focos rojos de riesgo de manera oportuna y ejecutar acciones basadas en evidencia estadística.")
    ]

    for titulo, desc in recoms:
        with st.container():
            st.markdown(f"**{titulo}**")
            st.markdown(f'<p class="custom-body" style="margin-bottom:18px;">{desc}</p>', unsafe_allow_html=True)