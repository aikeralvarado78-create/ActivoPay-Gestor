import streamlit as st

# Configuración de página
st.set_page_config(page_title="ActivoPay Gestor", layout="wide")

# Inicialización de conexión
conn = st.connection("postgresql", type="sql")

st.title("🚀 Gestión ActivoPay")

menu = st.sidebar.selectbox("Menú Principal", ["Dashboard", "Mis Clientes", "Carga Masiva"])

if menu == "Dashboard":
    st.subheader("Reporte de Gestión")
    # Consulta de prueba para verificar si el servidor responde
    try:
        with st.spinner("Conectando y probando base de datos..."):
            df = conn.query("SELECT 1 as test_conexion;")
            st.success("¡Conexión establecida! Servidor responde correctamente.")
            st.write("Resultado de prueba:", df)
    except Exception as e:
        st.error(f"Error al conectar: {e}")

elif menu == "Mis Clientes":
    st.subheader("Mis Clientes y Chat")
    st.write("Selecciona un cliente para ver su historial.")

elif menu == "Carga Masiva":
    st.subheader("Carga de Nuevos Clientes")
    uploaded_file = st.file_uploader("Cargar Excel", type=["xlsx"])
    if uploaded_file:
        st.success("Archivo subido.")
