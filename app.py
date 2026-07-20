import streamlit as st
from utils.database import ejecutar_consulta_limitada, get_global_date_range
from sessions import Introduccion, consultas_profesor, marco_metodologico, dict_DB, criticidad_temporal, delimitacion, delta_lake, demografia, ejemplo_filtrado, factores_riesgo, conclusiones

st.set_page_config(page_title="SWITRS California", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #1E1E1E; color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #2D2D2D; border-right: 2px solid #D4AF37; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 { color: #D4AF37 !important; text-align: center; }
        div[data-testid="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p { color: #FFFFFF; }
        div[data-testid="stRadio"] div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
            background-color: #D4AF37; border-color: #D4AF37;
        }
        hr { border: 1px solid #D4AF37; }
        .stDataFrame { border: 1px solid #D4AF37; }
    </style>
""", unsafe_allow_html=True)

if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "Presentación"

def cambiar_pag_pres(): st.session_state.pagina_actual = st.session_state.nav_pres
def cambiar_pag_expl(): st.session_state.pagina_actual = st.session_state.nav_expl
def cambiar_pag_query(): st.session_state.pagina_actual = st.session_state.nav_query
def cambiar_pag_ing(): st.session_state.pagina_actual = st.session_state.nav_ing

with st.sidebar:
    st.markdown("# 🚗 SWITRS Analítica")
    st.markdown("---")
    ver_pres = st.session_state.pagina_actual in ["Presentación", "Introducción", "Marco Metodológico", "Diccionario de datos", "Conclusiones"]
    ver_expl = st.session_state.pagina_actual in ["Perfil Demográfico", "Criticidad Temporal", "Factores de Riesgo"]
    ver_query = st.session_state.pagina_actual in ["Querys", "Querys de filtrado"]
    ver_ing = st.session_state.pagina_actual in ["Delta Lake", "Delimitacion de datos"]

    with st.expander("📖 1. Presentación", expanded=ver_pres):
        opciones_pres = ["Presentación", "Introducción", "Marco Metodológico", "Diccionario de datos", "Conclusiones"]
        idx_pres = opciones_pres.index(st.session_state.pagina_actual) if st.session_state.pagina_actual in opciones_pres else 0
        opcion_pres = st.radio("Menú Presentación:", opciones_pres, index=idx_pres, key="nav_pres", on_change=cambiar_pag_pres, label_visibility="collapsed")
        if st.session_state.pagina_actual in opciones_pres:
            st.session_state.pagina_actual = opcion_pres

    with st.expander("📊 2. Análisis Exploratorio", expanded=ver_expl):
        opciones_expl = ["Perfil Demográfico", "Criticidad Temporal", "Factores de Riesgo"]
        idx_expl = opciones_expl.index(st.session_state.pagina_actual) if st.session_state.pagina_actual in opciones_expl else 0
        opcion_expl = st.radio("Menú Exploratorio:", opciones_expl, index=idx_expl, key="nav_expl", on_change=cambiar_pag_expl, label_visibility="collapsed")
        if st.session_state.pagina_actual in opciones_expl:
            st.session_state.pagina_actual = opcion_expl

    with st.expander("🔍 3. Consultas (Querys)", expanded=ver_query):
        opciones_query = ["Querys", "Querys de filtrado"]
        idx_query = opciones_query.index(st.session_state.pagina_actual) if st.session_state.pagina_actual in opciones_query else 0
        opcion_query = st.radio("Menú Querys:", opciones_query, index=idx_query, key="nav_query", on_change=cambiar_pag_query, label_visibility="collapsed")
        if st.session_state.pagina_actual in opciones_query:
            st.session_state.pagina_actual = opcion_query

    with st.expander("🛠️ 4. Ingeniería y Limpieza", expanded=ver_ing):
        opciones_ing = ["Delta Lake", "Delimitacion de datos"]
        idx_ing = opciones_ing.index(st.session_state.pagina_actual) if st.session_state.pagina_actual in opciones_ing else 0
        opcion_ing = st.radio("Menú Ingeniería:", opciones_ing, index=idx_ing, key="nav_ing", on_change=cambiar_pag_ing, label_visibility="collapsed")
        if st.session_state.pagina_actual in opciones_ing:
            st.session_state.pagina_actual = opcion_ing

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📊 Periodo")
    st.caption("Seleccione el entorno:")

    filtro_etapa = st.radio(
        "Entorno cronológico:",
        ["Histórico Completo", "Pandemia", "Post-Pandemia"],
        label_visibility="collapsed"
    )

    fecha_inicio_exacta = None
    fecha_fin_exacta = None
    filtro_anio = "Todos"

    if filtro_etapa == "Pandemia":
        filtro_anio = "Todos"
        fecha_inicio_exacta = "2020-03-19"
        fecha_fin_exacta = "2021-01-24"
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("📅 **Corte: 19/Mar/2020 al 24/Ene/2021**")

    elif filtro_etapa == "Post-Pandemia":
        filtro_anio = 2021
        fecha_inicio_exacta = "2021-01-25"
        fecha_fin_exacta = "2021-12-31"
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("📅 **Corte: Desde 25/Ene/2021 en adelante**")

    else:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### Filtrado por año")
        opciones_anio = ["Todos", 2018, 2019, 2020, 2021]
        filtro_anio = st.selectbox("Año de análisis:", opciones_anio, index=0)
        min_date_global, max_date_global = get_global_date_range()
        fecha_inicio_exacta = min_date_global
        fecha_fin_exacta = max_date_global
        if filtro_anio != "Todos":
            fecha_inicio_exacta = f"{filtro_anio}-01-01"
            fecha_fin_exacta = f"{filtro_anio}-12-31"

fecha_ini = fecha_inicio_exacta
fecha_fin = fecha_fin_exacta

opcion = st.session_state.pagina_actual

if opcion == "Presentación":
    st.markdown("""
    <div style="background-color: #121212; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 20px;">
        <h1 style="color: #D4AF37; margin: 0;">🚗 SWITRS: Presentación Principal</h1>
        <p style="color: #FFFFFF; font-size: 18px; margin-top: 5px;">
            <span style="color: #D4AF37; font-weight: bold;">Datos de siniestralidad en California</span> · 
            Análisis exploratorio y visualizaciones interactivas
        </p>
        <p style="color: #CCCCCC; margin-bottom: 0;">
            Fuente: <span style="color: #D4AF37;">California Highway Patrol</span> – SWITRS
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.image("assets/analisis.png", caption="Análisis Estadístico del Sistema de Registro de Colisiones de California", use_container_width=True)
    st.markdown(f"<div style='text-align: center; color: #FFFFFF; font-size: 18px;'>Entorno: <span style='color: #D4AF37;'>{filtro_etapa}</span> ({fecha_ini} a {fecha_fin})</div>", unsafe_allow_html=True)
    sql_muestra = f"SELECT * FROM collisions WHERE collision_date BETWEEN '{fecha_ini}' AND '{fecha_fin}' LIMIT 50"
    df_muestra = ejecutar_consulta_limitada(sql_muestra, limite=50)
    st.dataframe(df_muestra, use_container_width=True)
    st.caption("Mostrando primeras 50 filas del periodo seleccionado.")


elif opcion == "Introducción":
    st.image("assets/introduccion_proyecto.png", use_container_width=True)
    Introduccion.mostrar_introduccion()
    
elif opcion == "Marco Metodológico":
    st.image("assets/metodologico.png", use_container_width=True)
    marco_metodologico.mostrar_marco_metodologico()
elif opcion == "Diccionario de datos":
    st.image("assets/diccionario.png", use_container_width=True)
    dict_DB.mostrar_diccionario_datos()
elif opcion == "Conclusiones":
    st.image("assets/conclusiones_real.png", use_container_width=True)
    conclusiones.mostrar_conclusiones()
elif opcion == "Perfil Demográfico":
    demografia.mostrar_demografia(fecha_ini, fecha_fin)
elif opcion == "Criticidad Temporal":
    criticidad_temporal.mostrar_criticidad(fecha_ini, fecha_fin)
elif opcion == "Factores de Riesgo":
    factores_riesgo.mostrar_factores_riesgo(fecha_ini, fecha_fin)
elif opcion == "Delta Lake":
    st.image("assets/delta lake.png", use_container_width=True)
    delta_lake.mostrar_delta_lake()
elif opcion == "Delimitacion de datos":
    st.image("assets/delimitacion.png", use_container_width=True)
    delimitacion.mostrar_delimitacion()
elif opcion == "Querys":
    import importlib
    import sessions.consultas_profesor as consultas
    importlib.reload(consultas)
    consultas.mostrar_consultas()
    st.image("assets/querys.png", use_container_width=True)
elif opcion == "Querys de filtrado":
    import importlib
    import sessions.ejemplo_filtrado as filtrado
    importlib.reload(filtrado)
    st.image("assets/filtrado.png", use_container_width=True)
    filtrado.mostrar_querys_filtrado()