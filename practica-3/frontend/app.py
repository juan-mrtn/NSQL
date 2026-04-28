import streamlit as st
import requests

st.set_page_config(page_title="Turismo App", layout="wide")
st.title("📍 Guía Turística NSQL")

# Le pegamos al contenedor del backend (por su nombre en Docker)
try:
    respuesta = requests.get("http://api-backend:8000/")
    if respuesta.status_code == 200:
        st.success(f"Conexión con la API exitosa: {respuesta.json()['mensaje']}")
except Exception as e:
    st.error("No se pudo conectar con el Backend todavía.")
