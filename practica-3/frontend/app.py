import streamlit as st
import requests
import pandas as pd

# Configuración básica
st.set_page_config(page_title="Turismo App", layout="centered")
st.title("Guía Turística NSQL")

# URL de la API (apunta al nombre del contenedor definido en Docker)
API_URL = "http://api-backend:8000"

# Coordenadas por defecto (Centro de Concordia para facilitar las pruebas)
DEFAULT_LAT = -31.3931
DEFAULT_LON = -58.0169

CATEGORIAS = ["cervecerias", "universidades", "farmacias", "emergencias", "supermercados"]

# Usamos pestañas (tabs) para separar la lógica visualmente
tab_agregar, tab_buscar, tab_distancia = st.tabs([
    "Agregar Lugar", 
    "Buscar Cercanos", 
    "Calcular Distancia"
])

# --- PESTAÑA 1: AGREGAR LUGAR ---
with tab_agregar:
    st.subheader("Cargar nuevo punto de interés")
    
    with st.form("form_agregar"):
        categoria = st.selectbox("Categoría", CATEGORIAS)
        nombre = st.text_input("Nombre del lugar (Ej: Lagash, Farmacia Centro)")
        
        col1, col2 = st.columns(2)
        with col1:
            latitud = st.number_input("Latitud", value=DEFAULT_LAT, format="%.6f")
        with col2:
            longitud = st.number_input("Longitud", value=DEFAULT_LON, format="%.6f")
            
        btn_guardar = st.form_submit_button("Guardar en Redis", type="primary")
        
        if btn_guardar:
            if nombre:
                payload = {
                    "categoria": categoria,
                    "nombre": nombre,
                    "latitud": latitud,
                    "longitud": longitud
                }
                try:
                    res = requests.post(f"{API_URL}/lugares", json=payload)
                    if res.status_code == 200:
                        st.success(res.json()["mensaje"])
                    else:
                        st.error("Error al guardar el lugar.")
                except requests.exceptions.ConnectionError:
                    st.error("No se pudo conectar con la API. ¿Está corriendo el backend?")
            else:
                st.warning("El nombre del lugar es obligatorio.")

# --- PESTAÑA 2: BUSCAR CERCANOS ---
with tab_buscar:
    st.subheader("Lugares a menos de 5km")
    
    cat_buscar = st.selectbox("¿Qué estás buscando?", CATEGORIAS, key="busq_cat")
    
    st.write("Tu ubicación actual:")
    col3, col4 = st.columns(2)
    with col3:
        mi_lat = st.number_input("Mi Latitud", value=DEFAULT_LAT, format="%.6f", key="mi_lat")
    with col4:
        mi_lon = st.number_input("Mi Longitud", value=DEFAULT_LON, format="%.6f", key="mi_lon")
        
    if st.button("Buscar en mi radio"):
        try:
            # Llamamos al endpoint GET pasando los parámetros por URL
            res = requests.get(f"{API_URL}/lugares/cercanos", params={"categoria": cat_buscar, "lat": mi_lat, "lon": mi_lon})
            
            if res.status_code == 200:
                datos = res.json()["lugares_en_radio"]
                if datos:
                    st.success(f"¡Encontramos {len(datos)} lugares!")
                    
                    # Convertimos a DataFrame para que Streamlit lo muestre como una tabla linda
                    df = pd.DataFrame(datos)
                    # Redondeamos la distancia para que quede prolija
                    df['distancia_km'] = df['distancia_km'].round(2) 
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No hay lugares de esta categoría en un radio de 5km.")
        except Exception:
            st.error("Error de conexión con la API.")

# --- PESTAÑA 3: CALCULAR DISTANCIA ---
with tab_distancia:
    st.subheader("Distancia exacta a un punto")
    
    cat_dist = st.selectbox("Categoría del destino", CATEGORIAS, key="dist_cat")
    destino = st.text_input("Nombre exacto del lugar guardado")
    
    if st.button("Calcular"):
        if destino:
            try:
                res = requests.get(f"{API_URL}/lugares/distancia", params={
                    "categoria": cat_dist, 
                    "lugar_nombre": destino, 
                    "lat": mi_lat, # Reutilizamos la latitud del panel anterior
                    "lon": mi_lon  # Reutilizamos la longitud del panel anterior
                })
                
                if res.status_code == 200:
                    data = res.json()
                    dist = round(data["distancia_km"], 2)
                    st.metric(label=f"Distancia a {destino}", value=f"{dist} km")
                elif res.status_code == 404:
                    st.warning("El lugar no existe o está mal escrito. Respetá mayúsculas y minúsculas.")
            except Exception:
                st.error("Error de conexión con la API.")
        else:
            st.warning("Tenés que escribir el nombre del lugar.")