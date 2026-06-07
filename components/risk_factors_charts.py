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

def render_tendencia_alcohol_mensual(df_tendencia):
    """
    df_tendencia tiene columnas: fecha (datetime), condicion, conteo
    """
    fig = px.line(df_tendencia, x='fecha', y='conteo', color='condicion',
                  markers=True, line_shape='linear',
                  color_discrete_map={'Con Alcohol': COFFEE, 'Sobrio': GOLD, 'Otro/Desconocido': '#666666'},
                  title='Evolución Mensual de Accidentes según Condición')
    fig.update_layout(
        title=dict(text='Evolución Mensual de Accidentes según Condición', font=dict(color=GOLD)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COFFEE),
        xaxis=dict(title='Mes', gridcolor='#333', tickfont=dict(color=COFFEE)),
        yaxis=dict(title='Cantidad de Accidentes', gridcolor='#333', tickfont=dict(color=COFFEE)),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD)
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
                 barmode='group')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COFFEE),
        xaxis_tickangle=-45,
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD),
        title=dict(font=dict(color=GOLD))
    )
    return fig

def render_boxplot_edad_por_tipo_colision(df_stats):
    """
    df_stats tiene columnas: type_of_collision, min, q1, median, q3, max
    Usamos px.box con los estadísticos precalculados (no cajas superpuestas)
    """
    # Creamos un DataFrame largo para que px.box entienda los cuartiles
    data = []
    for _, row in df_stats.iterrows():
        data.append({
            'type_of_collision': row['type_of_collision'],
            'min': row['min'],
            'q1': row['q1'],
            'median': row['median'],
            'q3': row['q3'],
            'max': row['max']
        })
    df_long = pd.DataFrame(data)
    # Para px.box necesitamos los valores reales, pero podemos usar go.Box con estadísticos (sin superposición)
    fig = go.Figure()
    for _, row in df_stats.iterrows():
        fig.add_trace(go.Box(
            name=row['type_of_collision'],
            q1=[row['q1']],
            median=[row['median']],
            q3=[row['q3']],
            lowerfence=[row['min']],
            upperfence=[row['max']],
            boxpoints=False,
            orientation='v'
        ))
    fig.update_layout(
        title=dict(text='Distribución de Edad de Víctimas por Tipo de Colisión', font=dict(color=GOLD)),
        xaxis_title='Tipo de Colisión',
        yaxis_title='Edad de la Víctima',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COFFEE),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD),
        boxmode='group'  # para que no se superpongan
    )
    return fig