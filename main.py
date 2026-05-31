import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# 1. Configuración de página
st.set_page_config(page_title="ActivoPay Gestor", layout="wide")

# 2. Configuración de conexión (usando SQLAlchemy para guardar datos)
# Asegúrate de poner tu URL real en los Secrets de Streamlit
try:
    url_db = st.secrets["connections"]["postgresql"]["url"]
    engine = create_engine(url_db)
except:
    engine = None

st.title("🚀 Gestión ActivoPay")

menu = st.sidebar.selectbox("Menú Principal", ["Dashboard", "Mis Clientes", "Carga Masiva"])

# 3. Lógica del Dashboard (Aquí veremos los datos guardados)
if menu == "Dashboard":
    st.subheader("Reporte de Gestión")
    if engine:
        try:
            df = pd.read_sql("SELECT * FROM clientes", engine)
            st.write("Base de datos de Clientes:", df)
        except:
            st.info("Aún no hay datos guardados en la base de datos.")
    else:
        st.error("Conexión a base de datos no configurada.")

# 4. Lógica de Carga Masiva (Para guardar los datos)
elif menu == "Carga Masiva":
    st.subheader("Carga de Nuevos Clientes")
    uploaded_file = st.file_uploader("Cargar Excel", type=["xlsx"])
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.write("Vista previa:", df.head())
        
        if st.button("Guardar en Base de Datos"):
            if engine:
                try:
                    # Esto guarda el Excel en la tabla 'clientes'
                    df.to_sql('clientes', engine, if_exists='append', index=False)
                    st.success("¡Datos guardados permanentemente!")
                except Exception as e:
                    st.error(f"Error al guardar: {e}")
            else:
                st.error("No hay conexión activa a la BD.")
