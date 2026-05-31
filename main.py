import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="ActivoPay Gestor", layout="wide")

# 2. Inicialización de conexión forzando IPv4
# El secreto 'postgresql' debe existir en tus ajustes de Streamlit
try:
    conn = st.connection("postgresql", type="sql")
    st.title("🚀 Gestión ActivoPay")
    
    # 3. Navegación
    menu = st.sidebar.selectbox("Menú Principal", ["Dashboard", "Mis Clientes", "Carga Masiva"])

    if menu == "Dashboard":
        st.subheader("Reporte de Gestión")
        with st.spinner("Conectando a la base de datos..."):
            # Consulta de prueba para verificar conectividad
            df = conn.query("SELECT 1 as test_conexion;", ttl=0)
            st.success("¡Conexión establecida!")
            st.write("Estado del servidor:", df)

except Exception as e:
    st.error(f"Error crítico de red: {e}")
    st.info("Nota: Si persiste, es una restricción de IP en tu proveedor de red.")
