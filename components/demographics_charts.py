import plotly.express as px
import pandas as pd

# PALETA DE COLORES CINESTÉSICA (DORADO & MODO OSCURO)

GOLD = "#D4AF37"          
GOLD_LIGHT = "#E6C687"    
CREMA = "#F4EBD0"         
TEXT_COLOR = "#FFFFFF"    
DARK_BG = "#121212"       
GRID_COLOR = "#2B261D"

def render_piramide_poblacional(df_agregado):
    df_pivot = df_agregado.pivot(index='rango_edad', columns='victim_sex', values='cantidad').fillna(0)
    df_pivot['male'] = -df_pivot['male']
    df_plot = df_pivot.reset_index().melt(id_vars='rango_edad', var_name='victim_sex', value_name='Cantidad')
    
    edad_order = ['0-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39',
                  '40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','80-84','85+']
    df_plot['rango_edad'] = pd.Categorical(df_plot['rango_edad'], categories=edad_order, ordered=True)
    
    fig = px.bar(df_plot, x='Cantidad', y='rango_edad', color='victim_sex',
                 orientation='h', color_discrete_map={'female': GOLD, 'male': GOLD_LIGHT},
                 labels={'rango_edad': 'Rango de Edad', 'Cantidad': 'Cantidad de Víctimas'})
    fig.update_layout(
        title=dict(text='Distribución Poblacional de Víctimas', font=dict(color=GOLD, size=20)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=CREMA),
        xaxis=dict(title='Cantidad', tickformat=',d', gridcolor=GRID_COLOR, tickfont=dict(color=CREMA)),
        yaxis=dict(gridcolor=GRID_COLOR, title=None, tickfont=dict(color=CREMA)),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD)
    )
    return fig

def render_distribucion_sexo(df_agregado):
    fig = px.pie(df_agregado, values='total', names='genero', hole=0.5,
                 color='genero', color_discrete_map={'Female': GOLD, 'Male': GOLD_LIGHT})
    fig.update_traces(textfont_color=TEXT_COLOR,
                      marker=dict(line=dict(color=DARK_BG, width=2)))
    fig.update_layout(
        title=dict(text='Participación por Género', font=dict(color=GOLD, size=18)),
        paper_bgcolor='rgba(0,0,0,0)', font=dict(color=CREMA),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor=DARK_BG, bordercolor=GOLD)
    )
    return fig
