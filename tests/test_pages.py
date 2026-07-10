import pytest
from streamlit.testing.v1 import AppTest

def test_app_loading():
    at = AppTest.from_file("app.py")
    at.run(timeout=15)  # <-- aumentar timeout

def test_demografia_page():
    at = AppTest.from_file("app.py")
    at.session_state.pagina_actual = "Perfil Demográfico"
    at.run(timeout=15)

def test_factores_riesgo_page():
    at = AppTest.from_file("app.py")
    at.session_state.pagina_actual = "Factores de Riesgo"
    at.run(timeout=15)