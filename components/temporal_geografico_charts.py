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