import plotly.express as px
import pandas as pd

GOLD = "#D4AF37"
COFFEE = "#4B3621"
DARK_BG = "#121212"
TEXT_COLOR = "#FFFFFF"

def render_areas_severidad(df_agregado):
    fig = px.area(df_agregado, x='anio', y='conteo', color='severidad',
                  color_discrete_map={
                      'Fatal': COFFEE, 'Lesión Grave': '#8B4513',
                      'Lesión Leve': '#CD853F', 'Solo Daños': GOLD, 'Otro': '#666666'
                  },
                  line_shape='linear')
    fig.update_layout(
        title=dict(text='Evolución de Accidentes por Severidad', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COFFEE),
        xaxis=dict(title='Año', dtick=1, gridcolor='#333', tickfont=dict(color=COFFEE)),
        yaxis=dict(title='Cantidad de Accidentes', gridcolor='#333', tickfont=dict(color=COFFEE)),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD)
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
                        color_discrete_map={'Pre-pandemia': COFFEE, 'Pandemia': GOLD})
    fig.update_layout(
        title=dict(text='Factores de Riesgo: Pre‑pandemia vs Pandemia', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COFFEE),
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color=COFFEE, gridcolor='#333'),
            angularaxis=dict(color=COFFEE, gridcolor='#333')
        ),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD)
    )
    return fig

def render_waterfall_anual(df_agregado):
    fig = px.bar(df_agregado, x='anio', y='cambio', text='cambio',
                 color=['positivo' if x>=0 else 'negativo' for x in df_agregado['cambio']],
                 color_discrete_map={'positivo': GOLD, 'negativo': COFFEE})
    fig.update_traces(textposition='outside')
    fig.update_layout(
        title=dict(text='Cambio Interanual de Accidentes', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COFFEE),
        xaxis=dict(title='Año', gridcolor='#333', tickfont=dict(color=COFFEE)),
        yaxis=dict(title='Cambio en Cantidad', gridcolor='#333', tickfont=dict(color=COFFEE)),
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
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COFFEE),
        xaxis=dict(title='Fecha', gridcolor='#333'),
        yaxis=dict(title='Número de Fatalidades', gridcolor='#333'),
        title=dict(font=dict(color=GOLD))
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
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(
        title=dict(text='Accidentes por Condición Climática e Iluminación', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COFFEE),
        xaxis=dict(title='Condición Climática', gridcolor='#333', tickfont=dict(color=COFFEE), tickangle=-45),
        yaxis=dict(title='Número de Accidentes', gridcolor='#333', tickfont=dict(color=COFFEE)),
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
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(
        title=dict(text='Accidentes por Tipo de Superficie de la Vía e Iluminación', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COFFEE),
        xaxis=dict(title='Superficie de la Vía', gridcolor='#333', tickfont=dict(color=COFFEE), tickangle=-45),
        yaxis=dict(title='Número de Accidentes', gridcolor='#333', tickfont=dict(color=COFFEE)),
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
        color_continuous_scale='Plasma',  # escala más vistosa
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
            line=dict(width=1, color='white'),
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
        font=dict(color=COFFEE, size=12),
        xaxis=dict(
            title=dict(font=dict(color=GOLD)),
            gridcolor='#333333',
            tickfont=dict(color=COFFEE),
            tickangle=-45
        ),
        yaxis=dict(
            title=dict(font=dict(color=GOLD)),
            gridcolor='#333333',
            tickfont=dict(color=COFFEE)
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
            tickfont=dict(color=COFFEE),
            title_font=dict(color=GOLD)
        )
    )
    return fig