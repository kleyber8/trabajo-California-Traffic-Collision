import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

GOLD = "#D4AF37"
COFFEE = "#4B3621"
DARK_BG = "#121212"
TEXT_COLOR = "#FFFFFF"

def render_severidad_vs_equipo(df_agregado):
    fig = px.bar(df_agregado, x='equipo', y='conteo', color='severidad',
                 barmode='group', 
                 color_discrete_sequence=[COFFEE, GOLD, '#8B4513', '#CD853F', '#666666'],
                 labels={'equipo': 'Equipo de Seguridad', 'conteo': 'Víctimas', 'severidad': 'Severidad'})
    fig.update_layout(
        title=dict(text='Severidad según Equipo de Seguridad', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COFFEE), xaxis_tickangle=-45,
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD)
    )
    return fig

def render_tendencia_alcohol_anual(df_agregado):
    fig = px.line(df_agregado, x='anio', y='conteo', color='condicion',
                  markers=True, line_shape='linear',
                  color_discrete_map={'Con Alcohol': COFFEE, 'Sobrio': GOLD, 'Otro/Desconocido': '#666666'})
    fig.update_layout(
        title=dict(text='Evolución Anual de Accidentes según Condición', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COFFEE),
        xaxis=dict(title='Año', gridcolor='#333', tickfont=dict(color=COFFEE)),
        yaxis=dict(title='Cantidad de Accidentes', gridcolor='#333', tickfont=dict(color=COFFEE)),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD)
    )
    return fig

def render_mapa_california(df_puntos):
    fig = px.scatter_mapbox(df_puntos, lat='latitude', lon='longitude',
                            color='collision_severity',
                            size='killed_victims', size_max=10,
                            zoom=5, center=dict(lat=36.7783, lon=-119.4179),
                            mapbox_style='carto-darkmatter',
                            hover_data={'case_id': True, 'collision_date': True})
    fig.update_layout(
        title=dict(text='Accidentes Fatales en California', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COFFEE),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD)
    )
    return fig

def render_boxplot_edad_por_tipo_colision(df_agregado):
    fig = px.box(df_agregado, x='type_of_collision', y='victim_age', color='victim_sex',
                 color_discrete_map={'male': COFFEE, 'female': GOLD},
                 labels={'type_of_collision': 'Tipo de Colisión', 'victim_age': 'Edad de la Víctima'})
    fig.update_layout(
        title=dict(text='Distribución de Edad de Víctimas por Tipo de Colisión', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COFFEE), xaxis_tickangle=-45,
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD)
    )
    return fig