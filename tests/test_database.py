import pytest
import pandas as pd
from utils.database import (
    get_md_connection,
    ejecutar_consulta,
    ejecutar_consulta_limitada,
    get_piramide_poblacional,
    get_distribucion_sexo
)

def test_connection():
    """Verifica que la conexión a MotherDuck funciona."""
    conn = get_md_connection()
    assert conn is not None
    df = conn.execute("SELECT 1 as test").df()
    assert df.iloc[0]['test'] == 1

def test_ejecutar_consulta():
    """Prueba que ejecutar_consulta devuelve un DataFrame."""
    df = ejecutar_consulta("SELECT 1 as num")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_ejecutar_consulta_limitada():
    """Prueba que la consulta limitada añade LIMIT correctamente."""
    df = ejecutar_consulta_limitada("SELECT * FROM collisions", limite=5)
    assert len(df) <= 5

def test_piramide_poblacional():
    """Prueba que la pirámide devuelve datos con las columnas esperadas."""
    df = get_piramide_poblacional('2018-01-01', '2021-12-31')
    assert not df.empty
    expected_cols = ['victim_sex', 'rango_edad', 'cantidad']
    assert all(col in df.columns for col in expected_cols)

def test_distribucion_sexo():
    """Prueba que la distribución de sexo devuelve las columnas esperadas."""
    df = get_distribucion_sexo('2018-01-01', '2021-12-31')
    assert not df.empty
    expected_cols = ['genero', 'total']
    assert all(col in df.columns for col in expected_cols)