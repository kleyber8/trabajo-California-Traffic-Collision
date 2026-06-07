import streamlit as st

def mostrar_delta_lake():
    st.markdown("""
    <div style="background-color: #121212; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 20px;">
        <h1 style="color: #D4AF37; margin: 0;">🐍 Delta Lake</h1>
        <p style="color: #FFFFFF; font-size: 18px; margin-top: 5px;">
            <span style="color: #D4AF37; font-weight: bold;">Almacenamiento transaccional en Data Lakes</span> · 
            Versionado y optimización de datos
        </p>
        <p style="color: #CCCCCC; margin-bottom: 0;">
            Fuente: <span style="color: #D4AF37;">California Highway Patrol</span> – SWITRS
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    
    st.header("Lógica detrás de la delimitación de la data")
    st.write("""
    Es un formato de almacenamiento que combina lo mejor de los Data Warehouses (orden y transacciones) con
    los Data Lakes (flexibilidad y gran volumen). Para evitar trabajar con CSV y Parquets sueltos utilizamos el
    Delta Lake que organiza los datos en tablas que mantienen un registro histórico de cada cambio.""")
    st.markdown("---")
    
    
    st.subheader("¿Por qué lo utilizamos?")
    st.write("""
            Debido a que no es posible subir la BD de SWITRS completa se utilizaron parquets (100.000 filas) de cada
            tabla a modo de ejemplo, de esta manera y utilizando el delta lake se guardo un registro/versiones de todos
            los cambios y filtrados que se realizaronn en la BD original""")
    st.markdown("---")
    
    st.info("Para ingresar al delta_Lake usamos la ruta 'data/delta_lake'")