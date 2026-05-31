import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="ActivoPay Gestor", layout="wide")

st.title("🚀 Gestión ActivoPay")

# 2. Sidebar para Navegación
menu = st.sidebar.selectbox("Menú Principal", ["Dashboard", "Mis Clientes", "Carga Masiva"])

# 3. Lógica del Dashboard
if menu == "Dashboard":
    st.subheader("Reporte de Gestión")
    st.info("Sistema listo. La base de datos está desconectada actualmente para desarrollo.")

# 4. Lógica de Mis Clientes
elif menu == "Mis Clientes":
    st.subheader("Mis Clientes y Chat")
    st.write("Selecciona un cliente para ver su historial.")

# 5. Lógica de Carga Masiva (Procesamiento de Excel)
elif menu == "Carga Masiva":
    st.subheader("Carga de Nuevos Clientes")
    uploaded_file = st.file_uploader("Cargar Excel", type=["xlsx"])
    
    if uploaded_file:
        try:
            # Leemos el archivo Excel con pandas (ahora con openpyxl instalado)
            df = pd.read_excel(uploaded_file)
            st.success("¡Archivo cargado con éxito!")
            st.write("Vista previa de los datos:")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
