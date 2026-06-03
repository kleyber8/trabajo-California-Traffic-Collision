import streamlit as st
from utils.database import obtener_datos
from sessions import Introduccion, querys, ejemplo_filtrado,dict_DB, criticidad_temporal, delimitacion,delta_lake, demografia, factores_riesgo
import pandas as pd

# Configuración de página
st.set_page_config(page_title="SWITRS California",
                page_icon="🚗",
                layout="wide")

# INYECCIÓN DE CSS GLOBAL (Dorado y Gris)
st.markdown("""
    <style>
        /* Fondo Principal */
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        
        /* Barra Lateral (Sidebar) */
        [data-testid="stSidebar"] {
            background-color: #2D2D2D;
            border-right: 2px solid #D4AF37;
        }
        
        /* Títulos en la Sidebar */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
            color: #D4AF37 !important;
            text-align: center;
        }

        /* Color Dorado para Radio Buttons Activos (Navegación) */
        div[data-testid="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
            color: #FFFFFF; /* Texto no seleccionado en blanco */
        }
        
        /* Estilo para la opción seleccionada */
        div[data-testid="stRadio"] div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
            background-color: #D4AF37; /* Fondo del círculo dorado */
            border-color: #D4AF37;
        }
        
        /* Divisores Dorados */
        hr {
            border: 1px solid #D4AF37;
        }
        
        /* Estilo para Dataframes (Tablas) */
        .stDataFrame {
            border: 1px solid #D4AF37;
        }
    </style>
""", unsafe_allow_html=True)

    
 # Inicialización del estado de navegación global (Evita conflictos entre expansores)
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "Presentación"

# Funciones de callback globales para cambiar de página al hacer clic en los radios
def cambiar_pag_pres(): st.session_state.pagina_actual = st.session_state.nav_pres
def cambiar_pag_expl(): st.session_state.pagina_actual = st.session_state.nav_expl
def cambiar_pag_query(): st.session_state.pagina_actual = st.session_state.nav_query
def cambiar_pag_ing(): st.session_state.pagina_actual = st.session_state.nav_ing

# 4. Construcción de la Barra Lateral (Sidebar)
with st.sidebar:
    st.markdown("# 🚗 SWITRS Analítica")
    st.markdown("---")

    # Determinar qué expander se abre automáticamente según la página activa
    ver_pres = st.session_state.pagina_actual in ["Presentación", "Introducción", "Diccionario de datos"]
    ver_expl = st.session_state.pagina_actual in ["Perfil Demográfico", "Criticidad Temporal", "Factores de Riesgo"]
    ver_query = st.session_state.pagina_actual in ["Querys", "Querys de filtrado"]
    ver_ing = st.session_state.pagina_actual in ["Delta Lake", "Delimitacion de datos"]
    
    # Variable temporal para capturar la selección del usuario en esta ejecución
    pagina_seleccionada = st.session_state.pagina_actual
    
    # --- CATEGORÍA 1: PRESENTACIÓN ---
    with st.expander("📖 1. Presentación", expanded=ver_pres):
        # Buscamos el índice actual seguro para que el radio no se resetee solo
        opciones_pres = ["Presentación", "Introducción", "Diccionario de datos"]
        idx_pres = opciones_pres.index(st.session_state.pagina_actual) if st.session_state.pagina_actual in opciones_pres else 0
        
        opcion_pres = st.radio(
            "Menú Presentación:",
            opciones_pres,
            index=idx_pres,
            key="nav_pres",
            on_change=cambiar_pag_pres,
            label_visibility="collapsed" 
        )
        if st.session_state.pagina_actual in opciones_pres:
            pagina_seleccionada = opcion_pres
            
    # --- CATEGORÍA 2: ANÁLISIS EXPLORATORIO ---
    with st.expander("📊 2. Análisis Exploratorio", expanded=ver_expl):
        opciones_expl = ["Perfil Demográfico", "Criticidad Temporal", "Factores de Riesgo"]
        idx_expl = opciones_expl.index(st.session_state.pagina_actual) if st.session_state.pagina_actual in opciones_expl else 0
        
        opcion_expl = st.radio(
            "Menú Exploratorio:",
            opciones_expl,
            index=idx_expl,
            key="nav_expl",
            on_change=cambiar_pag_expl,
            label_visibility="collapsed"
        )
        if st.session_state.pagina_actual in opciones_expl:
            pagina_seleccionada = opcion_expl
            
    # --- CATEGORÍA 3: QUERYS ---
    with st.expander("🔍 3. Consultas (Querys)", expanded=ver_query):
        opciones_query = ["Querys", "Querys de filtrado"]
        idx_query = opciones_query.index(st.session_state.pagina_actual) if st.session_state.pagina_actual in opciones_query else 0
        
        opcion_query = st.radio(
            "Menú Querys:",
            opciones_query,
            index=idx_query,
            key="nav_query",
            on_change=cambiar_pag_query,
            label_visibility="collapsed"
        )
        if st.session_state.pagina_actual in opciones_query:
            pagina_seleccionada = opcion_query
            
    # --- CATEGORÍA 4: INGENIERÍA Y LIMPIEZA ---
    with st.expander("🛠️ 4. Ingeniería y Limpieza", expanded=ver_ing):
        opciones_ing = ["Delta Lake", "Delimitacion de datos"]
        idx_ing = opciones_ing.index(st.session_state.pagina_actual) if st.session_state.pagina_actual in opciones_ing else 0
        
        opcion_ing = st.radio(
            "Menú Ingeniería:",
            opciones_ing,
            index=idx_ing,
            key="nav_ing",
            on_change=cambiar_pag_ing,
            label_visibility="collapsed"
        )
        if st.session_state.pagina_actual in opciones_ing:
            pagina_seleccionada = opcion_ing

    # Forzamos a que el estado global se sincronice con el último radio activo detectado
    st.session_state.pagina_actual = pagina_seleccionada
            
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📊 Periodo")
    st.caption("Seleccione el entorno:")
    
    # Selector de Entorno Cronológico Especial
    filtro_etapa = st.radio(
        "Entorno cronológico:",
        ["Histórico Completo", "Pandemia", "Post-Pandemia"],
        label_visibility="collapsed"
    )
    
    # Variables de control temporal internas (Fijas en código, invisibles en la UI)
    fecha_inicio_exacta = None
    fecha_fin_exacta = None
    filtro_anio = "Todos"
    
    # Lógica de mapeo automático según el botón seleccionado
    if filtro_etapa == "Pandemia":
        filtro_anio = "Todos"
        fecha_inicio_exacta = pd.to_datetime("2020-03-19")
        fecha_fin_exacta = pd.to_datetime("2021-01-24")
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("📅 **Corte: 19/Mar/2020 al 24/Ene/2021**")
        
    elif filtro_etapa == "Post-Pandemia":
        filtro_anio = 2021
        fecha_inicio_exacta = pd.to_datetime("2021-01-25")
        fecha_fin_exacta = pd.to_datetime("2021-12-31")
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("📅 **Corte: Desde 25/Ene/2021 en adelante**")
        
    else:
        # Si es Histórico Completo, habilitamos el selectbox clásico de año abajo
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### Filtrado por año")
        opciones_anio = ["Todos", 2018, 2019, 2020, 2021]
        filtro_anio = st.selectbox("Año de análisis:", opciones_anio, index=0)
        
# Lógica de "Páginas"
opcion = st.session_state.pagina_actual

# 1. Ejecutamos la carga y filtrado de datos GLOBAL aquí arriba una sola vez
with st.spinner("Filtrando datos según el periodo seleccionado..."):
    df_filtrado = obtener_datos("collisions", anio=filtro_anio)
    
    # Aplicación automática de las máscaras fijas de fecha al dataframe global
    if not df_filtrado.empty and (fecha_inicio_exacta is not None):
        df_filtrado['collision_date'] = pd.to_datetime(df_filtrado['collision_date'], errors='coerce')
        df_filtrado = df_filtrado[(df_filtrado['collision_date'] >= fecha_inicio_exacta) & (df_filtrado['collision_date'] <= fecha_fin_exacta)]

# 2. Ahora enviamos "df_filtrado" a la página que lo necesite
if opcion == "Presentación":
    st.markdown("<h1 style='color: #D4AF37; text-align: center; font-size: 40px;'>🚗 SWITRS: Presentación Principal</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.image(
        "assets/Copia de Introducción (1).png", 
        caption="Análisis Estadístico del Sistema de Registro de Colisiones de California",
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='text-align: center; color: #FFFFFF; font-size: 18px; margin-bottom: 20px;'>
            Entorno Metodológico Seleccionado: <span style='color: #D4AF37; font-weight: bold;'>{filtro_etapa}</span>
        </div>
    """, unsafe_allow_html=True)
    
    if not df_filtrado.empty:
        st.dataframe(df_filtrado.head(50), use_container_width=True)
        st.caption(f"Visualizando los primeros 50 registros de un universo de {len(df_filtrado):,} filas.")
    else:
        st.warning("No se encontraron registros para el rango de fechas específico.")
            
elif opcion == "Introducción":
    Introduccion.mostrar_introduccion()

elif opcion == "Diccionario de datos":
    dict_DB.mostrar_diccionario_datos()

elif opcion == "Perfil Demográfico":
    demografia.mostrar_demografia(df_filtrado)

elif opcion == "Criticidad Temporal":
    criticidad_temporal.mostrar_criticidad(df_filtrado)

elif opcion == "Factores de Riesgo":
    factores_riesgo.mostrar_factores_riesgo(df_filtrado)

elif opcion == "Delta Lake":
    delta_lake.mostrar_delta_lake()

elif opcion == "Delimitacion de datos":
    delimitacion.mostrar_delimitacion()

elif opcion == "Querys":
    querys.mostrar_querys()

elif opcion == "Querys de filtrado":
    ejemplo_filtrado.mostrar_querys_filtrado()