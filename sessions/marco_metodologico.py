import streamlit as st

def mostrar_marco_metodologico():
    st.markdown("""
    <div style="background-color: #121212; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 20px;">
        <h1 style="color: #D4AF37; margin: 0;">Marco Metodológico: Proyecto SWITRS</h1>
        <p style="color: #FFFFFF; font-size: 18px; margin-top: 5px;">
            <span style="color: #D4AF37; font-weight: bold;">Cómo se realizó la investigación, métodos, técnicas y herramientas utilizados para recolectar y analizar los datos.</span> · 
            Análisis de siniestralidad vial en California
        </p>
        <p style="color: #CCCCCC; margin-bottom: 0;">
            Fuente: <span style="color: #D4AF37;">California Highway Patrol</span> – SWITRS
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # --- SECCIÓN 1: PLANTEAMIENTO ---
    st.markdown("## 1.1 Planteamiento del Problema")
    st.markdown("""
    A nivel global, la seguridad vial representa uno de los desafíos de salud pública más críticos del siglo XXI. En los Estados Unidos, el estado de California es un referente en la adopción de regulaciones de tránsito estrictas, campañas de concienciación y la integración de tecnologías avanzadas de asistencia a la hora de conducir. 
                
    Sin embargo, la tecnología y las mejoras estructurales en los vehículos no son proporcionales en la reducción de la siniestralidad. California continúa registrando tasas alarmantes de fatalidades y lesiones graves en sus vías públicas, lo que evidencia que **el factor tecnológico vehicular es insuficiente si se evalúa de forma aislada** de los factores humanos, temporales y ambientales.
    """)

    # Nota destacada sobre la brecha analítica
    st.warning("""
    **La Brecha Analítica:** El estado cuenta con el *Statewide Integrated Traffic Records System* (SWITRS), una base de datos pública de alta dimensionalidad. A pesar de la disponibilidad de estos datos crudos, existe una marcada brecha analítica y operativa: las autoridades de tránsito, los planificadores urbanos y la ciudadanía carecen de herramientas interactivas, accesibles y de procesamiento exploratorio avanzado.
    """)

    st.markdown("""
    La mayoría de los reportes oficiales se limitan a análisis descriptivos unidimensionales o estáticos. No se trata únicamente de cuantificar dónde ocurren los accidentes (criticidad geográfica), sino de entender de forma interconectada **quiénes son los afectados y bajo qué condiciones específicas se determina la supervivencia** en un impacto.
                
    Por lo tanto, es menester el análisis de esta problemática y su solvencia mediante herramientas tecnológicas como **Streamlit** y **Power BI** para lograr un reporte útil que refleje lo que la seguridad vial realmente necesita observar para mejorar futuras condiciones de ese sector, no solo en California, sino del mundo.
    """)
    st.divider()

    # --- SECCIÓN 2: JUSTIFICACIÓN Y DISEÑO ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 1.2 Justificación")
        st.markdown("""
        De no desarrollarse metodologías que sistematicen, procesen y visualicen dinámicamente la información de SWITRS, las decisiones de infraestructura y patrullaje seguirán tomándose bajo **enfoques reactivos y no preventivos**. 
        
        Se mantendrá la invisibilización de patrones demográficos críticos (como la concentración de mortalidad en ciertos rangos de edad) y se subestimará el impacto real de las conductas de riesgo en la severidad de las lesiones. La transmisión de estos análisis es estrictamente necesaria para reducir los índices de mortalidad vial en el estado.
        """)

    with col2:
        st.markdown("## 1.3 Tipo y Nivel de Investigación")
        st.markdown("""
        * **Tipo de Investigación:** **Documental**, puesto que el proceso de recolección de información se fundamenta en la obtención, análisis e interpretación de datos secundarios provenientes del registro masivo de SWITRS.
        
        * **Nivel de la Investigación:** **Descriptivo-Correlacional**. 
            * Es *descriptivo* debido a que se propone caracterizar y perfilar el comportamiento del fenómeno vial. 
            * Alcanza un nivel *correlacional* por cuanto busca determinar el grado de asociación, relación e impacto que ejercen factores de riesgo específicos sobre la severidad y supervivencia en las colisiones registradas.
        """)

    st.divider()

    # --- SECCIÓN 3: OBJETIVOS Y PREGUNTA ---
    st.markdown("## 1.4 Enfoque de la Investigación")
    
    # Cuadro destacado para el Objetivo General
    st.info("""
    🎯 **Objetivo General** Desarrollar un análisis de datos sobre la siniestralidad vial en California (2018-2021), centrado en la identificación de perfiles de vulnerabilidad y factores de riesgo mediante arquitecturas analíticas modernas.
    """)

    # Bloque de cita para la Pregunta General
    st.markdown("> **Pregunta General de Investigación:**")
    st.markdown("""
    *¿Cómo configurar un análisis exploratorio y visual de datos sobre la siniestralidad vial en California entre 2018 y 2021 que permita identificar con precisión los perfiles de vulnerabilidad de las víctimas y la influencia de los factores de riesgo conductuales?*
    """)
    st.write("")

    st.markdown("### Objetivos Específicos")
    
    # Lista organizada con negritas estratégicas para los campos de datos
    st.markdown("""
    1. **Analizar el perfil demográfico de las víctimas:** Construir una pirámide de mortalidad segmentada por edad (`victim_age`) y sexo (`victim_sex`) para identificar qué grupos poblacionales sufren mayor impacto en colisiones fatales.
    2. **Determinar factores externos determinantes de una colisión:** Evaluar cuantitativamente el impacto de las conductas de riesgo (`cellphone_in_use`, `party_sobriety`, entre otros) y la eficacia del equipo de seguridad (`victim_safety_equipment`) en la severidad de las lesiones y la ocurrencia de víctimas fatales.
    3. **Visualizar la criticidad geográfica y temporal:** Mapear geoespacialmente los incidentes, evaluar su evolución anual y comparar analíticamente el efecto en los periodos pre-pandemia y pandemia.
    """)

    st.divider()
    
    # Nota al pie metodológica
    st.caption("Marco Metodológico generado para la sustentación académica del proyecto. Datos fuente extraídos de SWITRS California.")