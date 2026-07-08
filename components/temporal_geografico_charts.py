import plotly.express as px
import pandas as pd

# PALETA DE COLORES CINESTÉSICA (DORADO & MODO OSCURO)
GOLD = "#D4AF37"              
GOLD_DARK = "#9A7B3E"  
GOLD_LIGHT = "#E6C687"
GOLD_MUTED = "#C5A059"  
CREMA = "#F4EBD0"         
TEXT_COLOR = "#FFFFFF"    
DARK_BG = "#121212"       
GRID_COLOR = "#2B261D"
TERRACOTA = "#bc6c25"       
CREMA_CLARO = "#fdfcdc"   
VAINILLA = "#faedcd"      
GRIS_OSCURO = "#444444"   
AZUL_PROFUNDO = "#004e89" 

# Escala secuencial de dorados para gráficos de barras y mapas térmicos
PALETA_DORADOS = [GOLD_DARK, TERRACOTA, AZUL_PROFUNDO, GOLD]
DEGRADADO_BURBUJAS = [AZUL_PROFUNDO, GOLD_DARK, CREMA_CLARO, GOLD]

def render_areas_severidad(df_agregado):
    fig = px.area(df_agregado, x='anio', y='conteo', color='severidad',
                  color_discrete_map={
                      'Solo Daños': GOLD_DARK, 
                      'Lesión Leve': GOLD_MUTED,
                      'Lesión Grave': GOLD_LIGHT, 
                      'Fatal': GOLD, 
                      'Otro': '#444444'
                  },
                  line_shape='linear')
    fig.update_layout(
        title=dict(text='Evolución de Accidentes por Severidad', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=CREMA),
        xaxis=dict(title='Año', dtick=1, gridcolor='#333', tickfont=dict(color=CREMA)),
        yaxis=dict(title='Cantidad de Accidentes', gridcolor='#333', tickfont=dict(color=CREMA)),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD, borderwidth=1)
    )
    return fig

def render_radar_factores(df_pre, df_pan):
    categorias = ['Alcohol', 'Drogas', 'Celular', 'Clima Adverso', 'Oscuridad']
    pre_vals = [df_pre.iloc[0]['alcohol'], df_pre.iloc[0]['drogas'], df_pre.iloc[0]['celular'],
                df_pre.iloc[0]['clima_adverso'], df_pre.iloc[0]['oscuridad']]
    pan_vals = [df_pan.iloc[0]['alcohol'], df_pan.iloc[0]['drogas'], df_pan.iloc[0]['celular'],
                df_pan.iloc[0]['clima_adverso'], df_pan.iloc[0]['oscuridad']]
    data = []
    for i, cat in enumerate(categorias):
        data.append({'Factor': cat, 'Periodo': 'Pre-pandemia', 'Porcentaje': pre_vals[i]})
        data.append({'Factor': cat, 'Periodo': 'Pandemia', 'Porcentaje': pan_vals[i]})
    df_radar = pd.DataFrame(data)
    fig = px.line_polar(df_radar, r='Porcentaje', theta='Factor', color='Periodo',
                        line_close=True,
                        color_discrete_map={'Pre-pandemia': GOLD_MUTED, 'Pandemia': GOLD})
    fig.update_layout(
        title=dict(text='Factores de Riesgo: Pre‑pandemia vs Pandemia', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=CREMA),
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color=CREMA, gridcolor=GRID_COLOR),
            angularaxis=dict(color=CREMA, gridcolor= GRID_COLOR)
        ),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD, borderwidth=1)
    )
    return fig

def render_waterfall_anual(df_agregado):
    fig = px.bar(df_agregado, x='anio', y='cambio', text='cambio',
                 color=['positivo' if x>=0 else 'negativo' for x in df_agregado['cambio']],
                 color_discrete_map={'positivo': GOLD, 'negativo': GOLD_DARK})
    fig.update_traces(textposition='outside', textfont=dict(color=CREMA))
    fig.update_layout(
        title=dict(text='Cambio Interanual de Accidentes', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=CREMA),
        xaxis=dict(title='Año', gridcolor='#333', tickfont=dict(color=CREMA)),
        yaxis=dict(title='Cambio en Cantidad', gridcolor='#333', tickfont=dict(color=CREMA)),
        showlegend=False
    )
    return fig

def render_scatter_animado(df_agregado):
    fig = px.scatter_mapbox(df_agregado, lat='latitude', lon='longitude',
                            color='severidad', size='killed_victims',
                            animation_frame='anio', size_max=8,
                            zoom=5, center=dict(lat=36.7783, lon=-119.4179),
                            mapbox_style='carto-darkmatter',
                            labels={'severidad': 'Severidad'})
    fig.update_layout(
        title=dict(text='Evolución Geográfica de Accidentes Fatales', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT_COLOR),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD)
    )
    # Cambiar el color de los textos del slider de animación
    fig.layout.sliders[0].currentvalue.font.color = CREMA
    fig.layout.sliders[0].font.color = CREMA
    return fig

def render_tendencia_fatalidades(df_agregado):
    """
    df_agregado tiene columnas: fecha (datetime), fatalidades (acumuladas)
    """
    fig = px.line(
        df_agregado, x='fecha', y='fatalidades',
        title='Evolución de Fatalidades en el Tiempo',
        markers=True,
        line_shape='linear'
    )
    fig.update_traces(line=dict(color=GOLD, width=3), marker=dict(color=GOLD_LIGHT, size=6))
    fig.update_layout(
        title=dict(text='Evolución de Fatalidades en el Tiempo', font=dict(color=GOLD, size=16)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=CREMA),
        xaxis=dict(title='Fecha', gridcolor=GRID_COLOR, tickfont=dict(color=CREMA)),
        yaxis=dict(title='Número de Fatalidades', gridcolor=GRID_COLOR, tickfont=dict(color=CREMA))
    )
    return fig

def render_weather_lighting_grouped_bar(df_agregado):
    """
    Barras agrupadas: weather_1 en X, lighting como color, conteo en Y.
    """
    fig = px.bar(df_agregado, x='weather_1', y='conteo', color='lighting',
                 barmode='group',
                 title='Accidentes por Condición Climática e Iluminación',
                 labels={'weather_1': 'Condición Climática', 'conteo': 'Número de Accidentes', 'lighting': 'Iluminación'},
                 color_discrete_sequence=PALETA_DORADOS)
    fig.update_layout(
        title=dict(text='Accidentes por Condición Climática e Iluminación', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=CREMA),
        xaxis=dict(title='Condición Climática', gridcolor=GRID_COLOR, tickfont=dict(color=CREMA), tickangle=-45),
        yaxis=dict(title='Número de Accidentes', gridcolor=GRID_COLOR, tickfont=dict(color=CREMA)),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD)
    )
    return fig

def render_road_lighting_grouped_bar(df_agregado):
    """
    Barras agrupadas: road_surface en X, lighting como color, conteo en Y.
    """
    fig = px.bar(df_agregado, x='road_surface', y='conteo', color='lighting',
                 barmode='group',
                 title='Accidentes por Tipo de Superficie de la Vía e Iluminación',
                 labels={'road_surface': 'Superficie de la Vía', 'conteo': 'Número de Accidentes', 'lighting': 'Iluminación'},
                 color_discrete_sequence=PALETA_DORADOS)
    fig.update_layout(
        title=dict(text='Accidentes por Tipo de Superficie de la Vía e Iluminación', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=CREMA),
        xaxis=dict(title='Superficie de la Vía', gridcolor=GRID_COLOR , tickfont=dict(color=CREMA), tickangle=-45),
        yaxis=dict(title='Número de Accidentes', gridcolor=GRID_COLOR , tickfont=dict(color=CREMA)),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD)
    )
    return fig

def render_road_lighting_bubble(df_agregado):
    """
    Gráfico de burbujas mejorado:
    - Eje X: Iluminación
    - Eje Y: Superficie de la vía
    - Tamaño: número de accidentes
    - Color: número de accidentes (escala térmica)
    - Burbujas con borde blanco y transparencia
    """
    fig = px.scatter(
        df_agregado,
        x='lighting',
        y='road_surface',
        size='conteo',
        color='conteo',
        color_continuous_scale=DEGRADADO_BURBUJAS,  # escala más vistosa
        size_max=70,                      # burbujas más grandes
        title='Relación entre Superficie de la Vía e Iluminación en Accidentes',
        labels={
            'lighting': 'Condición de Iluminación',
            'road_surface': 'Tipo de Superficie',
            'conteo': 'Número de Accidentes'
        },
        hover_data={'conteo': ':,.0f'}
    )
    # Mejorar diseño
    fig.update_traces(
        marker=dict(
            line=dict(width=1, color=DARK_BG),
            opacity=0.8
        )
    )
    fig.update_layout(
        title=dict(
            text='Relación entre Superficie de la Vía e Iluminación en Accidentes',
            font=dict(color=GOLD, size=20),
            x=0.5  # centrar título
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=CREMA, size=12),
        xaxis=dict(
            title=dict(font=dict(color=GOLD)),
            gridcolor=GRID_COLOR,
            tickfont=dict(color=CREMA),
            tickangle=-45
        ),
        yaxis=dict(
            title=dict(font=dict(color=GOLD)),
            gridcolor=GRID_COLOR,
            tickfont=dict(color=CREMA)
        ),
        legend=dict(
            title=dict(text='Nº Accidentes', font=dict(color=GOLD)),
            font=dict(color=TEXT_COLOR),
            bgcolor=DARK_BG,
            bordercolor=GOLD,
            borderwidth=1
        ),
        coloraxis_colorbar=dict(
            title='Accidentes',
            tickfont=dict(color=CREMA),
            title_font=dict(color=GOLD)
        )
    )
    return fig