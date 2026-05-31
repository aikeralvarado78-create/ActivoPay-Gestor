import streamlit as st
import pandas as pd
import socket
from sqlalchemy import create_engine

# FORZAR IPv4: Esto evita el error "Cannot assign requested address"
socket.AF_INET = socket.AF_INET

# 1. Configuración de página
st.set_page_config(page_title="ActivoPay Gestor", layout="wide")

# 2. Configuración de motor de base de datos
try:
    # Asegúrate de que el nombre del secreto coincida exactamente con lo que pongas en los settings
    url_db = st.secrets["connections"]["postgresql"]["url"]
    engine = create_engine(url_db)
except Exception as e:
    engine = None
    st.sidebar.error("Error de configuración de conexión.")

st.title("🚀 Gestión ActivoPay")

menu = st.sidebar.selectbox("Menú Principal", ["Dashboard", "Mis Clientes", "Carga Masiva"])

# 3. Lógica del Dashboard
if menu == "Dashboard":
    st.subheader("Reporte de Gestión")
    if engine:
        try:
            df = pd.read_sql("SELECT * FROM clientes", engine)
            st.write("Base de datos de Clientes:", df)
        except Exception as e:
            st.info("Aún no hay datos guardados o la tabla no existe.")
    else:
        st.error("No se pudo conectar a la base de datos.")

# 4. Lógica de Carga Masiva
elif menu == "Carga Masiva":
    st.subheader("Carga de Nuevos Clientes")
    uploaded_file = st.file_uploader("Cargar Excel", type=["xlsx"])
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.write("Vista previa:", df.head())
        
        if st.button("Guardar en Base de Datos"):
            if engine:
                try:
                    df.to_sql('clientes', engine, if_exists='append', index=False)
                    st.success("¡Datos guardados permanentemente!")
                except Exception as e:
                    st.error(f"Error al guardar: {e}")
            else:
                st.error("No hay conexión activa.")
