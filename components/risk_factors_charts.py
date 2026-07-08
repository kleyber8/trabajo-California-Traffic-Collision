import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# PALETA DE COLORES AMPLIADA (DORADOS, TERROSOS Y CONTRASTE)

GOLD = "#D4AF37"          
GOLD_DARK = "#9A7B3E" 
CREMA = "#F4EBD0"         
TEXT_COLOR = "#FFFFFF"   
DARK_BG = "#121212"      
GRID_COLOR = "#2B261D"    
TERRACOTA = "#bc6c25"     
CHAMPAGNE = "#dda15e"     
CREMA_CLARO = "#fdfcdc"   
VAINILLA = "#faedcd"      
GRIS_OSCURO = "#444444"   
AZUL_PROFUNDO = "#004e89" 

PALETA_DORADOS = [GOLD, TERRACOTA, AZUL_PROFUNDO, GOLD, CREMA_CLARO, GRIS_OSCURO, CHAMPAGNE, GRID_COLOR, VAINILLA ]

MAPEO_SEVERIDAD = {
    # --- Categorías de Víctimas (Gráfico de Equipos de Seguridad) ---
    'no injury': GRIS_OSCURO,                 
    'complaint of pain': CHAMPAGNE,           
    'suspected minor injury': TERRACOTA,     
    'possible injury': VAINILLA,              
    'other visible injury': CREMA_CLARO,      
    'severe injury': GOLD_DARK,               
    'suspected serious injury': GOLD,        
    'killed': AZUL_PROFUNDO,              

    # --- Categorías de Accidentes (Otros gráficos del módulo) ---
    'property damage only': GRIS_OSCURO,
    'pain': CHAMPAGNE,
    'other injury': CREMA_CLARO,
    'severe injury': GOLD_DARK,
    'fatal': GOLD    
}

def render_severidad_vs_equipo(df_agregado):
    fig = px.bar(df_agregado, x='equipo', y='conteo', color='severidad',
                 barmode='group', 
                 color_discrete_map=MAPEO_SEVERIDAD,
                 labels={'equipo': 'Equipo de Seguridad', 'conteo': 'Víctimas', 'severidad': 'Severidad'})
    fig.update_layout(
        title=dict(text='Severidad según Equipo de Seguridad', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=CREMA), 
        xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=CREMA), tickangle=-45),
        yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=CREMA)),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD, borderwidth=1)
    )
    return fig


def render_barras_fatalidades(df_agregado):
    """
    df_agregado tiene columnas: condado, factor, fatalidades
    Barras agrupadas (barmode='group') como el primer gráfico
    """
    fig = px.bar(df_agregado, x='condado', y='fatalidades', color='factor',
                 title='Fatalidades por Condado y Factor de Colisión',
                 labels={'condado': 'Condado', 'fatalidades': 'Número de Fatalidades', 'factor': 'Factor de Colisión'},
                 color_discrete_sequence=PALETA_DORADOS,
                 barmode='group')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=CREMA),
        xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=CREMA), tickangle=-45),
        yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=CREMA)),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD, borderwidth=1),
        title=dict(font=dict(color=GOLD, size=16))
    )
    return fig

def render_boxplot_edad_por_tipo_colision(df_stats):
    """
    df_stats tiene columnas: type_of_collision, min, q1, median, q3, max
    Usa go.Box con estadísticos precalculados y boxmode='group' para evitar superposición.
    """
    fig = go.Figure()
    
    num_traces = len(df_stats)
    colores_cajas = [PALETA_DORADOS[i % len(PALETA_DORADOS)] for i in range(num_traces)]
    
    for idx, row in df_stats.iterrows():
        color_actual = colores_cajas[idx]
        fig.add_trace(go.Box(
            name=row['type_of_collision'],
            q1=[row['q1']],
            median=[row['median']],
            q3=[row['q3']],
            lowerfence=[row['min']],
            upperfence=[row['max']],
            boxpoints=False,
            orientation='v',
            marker_color=color_actual,
            line=dict(width=1.5),
            fillcolor=color_actual
        ))
    fig.update_layout(
        title=dict(text='Distribución de Edad de Víctimas por Tipo de Colisión', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=CREMA),
        xaxis=dict(title='Tipo de Colisión', gridcolor=GRID_COLOR, tickfont=dict(color=CREMA)),
        yaxis=dict(title='Edad de la Víctima', gridcolor=GRID_COLOR, tickfont=dict(color=CREMA)),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD, borderwidth=1),
        boxmode='group'
    )
    return fig

def render_tendencia_alcohol_mensual(df_tendencia):
    """
    df_tendencia tiene columnas: mes (datetime), condicion, conteo
    """
    fig = px.line(df_tendencia, x='mes', y='conteo', color='condicion',
                  markers=True, line_shape='linear',
                  color_discrete_map={'Con Alcohol': GOLD, 'Sobrio': CREMA_CLARO, 'Otro/Desconocido': TERRACOTA})
    fig.update_layout(
        title=dict(text='Evolución Mensual de Accidentes según Condición', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=CREMA),
        xaxis=dict(title='Mes', gridcolor=GRID_COLOR, tickfont=dict(color=CREMA)),
        yaxis=dict(title='Cantidad de Accidentes', gridcolor=GRID_COLOR, tickfont=dict(color=CREMA)),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD)
    )
    return fig

def render_vehicle_type_severity(df_agregado):
    """
    Barras agrupadas: tipos de vehículo en X, severidad como color, conteo como Y.
    """
    fig = px.bar(df_agregado, x='tipo_vehiculo', y='conteo', color='severidad',
                 barmode='group',
                 title='Top Tipos de Vehículo según Severidad de Accidente',
                 labels={'tipo_vehiculo': 'Tipo de Vehículo', 'conteo': 'Número de Accidentes', 'severidad': 'Severidad'},
                 color_discrete_map=MAPEO_SEVERIDAD)
    fig.update_layout(
        title=dict(font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=CREMA),
        xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=CREMA, size=10), tickangle=-45),
        yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=CREMA)),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD, borderwidth=1)
    )
    return fig

def render_vehicle_year_severity(df_agregado):
    """
    Gráfico de líneas o área (usamos área para mayor impacto visual).
    Muestra la evolución de accidentes por año del vehículo, segmentado por severidad.
    """
    fig = px.area(df_agregado, x='vehicle_year', y='conteo', color='severidad',
                  title='Evolución de Accidentes por Año del Vehículo y Severidad',
                  labels={'vehicle_year': 'Año de Fabricación', 'conteo': 'Número de Accidentes', 'severidad': 'Severidad'},
                  color_discrete_map=MAPEO_SEVERIDAD)
    fig.update_layout(
        title=dict(font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=CREMA),
        xaxis=dict(title='Año del Vehículo', gridcolor=GRID_COLOR, tickfont=dict(color=CREMA), tickangle=-45),
        yaxis=dict(title='Accidentes', gridcolor=GRID_COLOR, tickfont=dict(color=CREMA)),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD, borderwidth=1)
    )
    return fig