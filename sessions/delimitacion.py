import streamlit as st

def mostrar_delimitacion():
    st.markdown("""
    <div style="background-color: #121212; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 20px;">
        <h1 style="color: #D4AF37; margin: 0;">🔍 Delimitación de datos</h1>
        <p style="color: #FFFFFF; font-size: 18px; margin-top: 5px;">
            <span style="color: #D4AF37; font-weight: bold;">Criterios de selección y depuración</span> · 
            De 9.25 GB a 1.7 GB de información relevante
        </p>
        <p style="color: #CCCCCC; margin-bottom: 0;">
            Fuente: <span style="color: #D4AF37;">California Highway Patrol</span> – SWITRS
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    
    st.header("Lógica detrás de la delimitación de la data")
    st.write("""La base de datos switrs.sqlite contiene una recolección amplia de accidentes en el estado de California, con
            registros que datan de 2009 a 2021. Para delimitar la magnitud del análisis, primero se trabajó con la variable
            db_year, que indica el año en que se extrajeron los registros de California Highway Patrol (CHP) para esta data
            SWITRS (“California Traffic Collision Data”). De este campo se depuraron los años con menor volumen de información
            (específicamente 2016, 2017) y los datos de 2018, conservando la información recogida en 2020 y 2021, las cuales
            cubren colisiones ocurridas entre 2009 y 2021.""")
    
    st.write("""Posteriormente, se seleccionaron únicamente los incidentes de los últimos cuatro años con la variable de (collision_date).
            La elección de los campos se basó en su relación directa con los objetivos del estudio, incluyendo variables como 
            victim_sex, cellphone_in_use, collision_severity, entre otros...""")