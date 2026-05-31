import streamlit as st

# 1. Configuración obligatoria al inicio
st.set_page_config(page_title="ActivoPay Gestor", layout="wide")

# 2. Inicialización de la conexión con manejo de errores
try:
    conn = st.connection("postgresql", type="sql")
except Exception as e:
    st.error(f"Error fatal al iniciar la conexión: {e}")
    st.stop() # Detiene la ejecución si no hay BD

st.title("🚀 Gestión ActivoPay")

# 3. Navegación
menu = st.sidebar.selectbox("Menú Principal", ["Dashboard", "Mis Clientes", "Carga Masiva"])

# 4. Lógica de Dashboard con manejo de consultas
if menu == "Dashboard":
    st.subheader("Reporte de Gestión")
    try:
        # Consulta como cadena de texto simple para evitar problemas de caché
        df = conn.query("SELECT * FROM empresas LIMIT 10;")
        st.write("Resumen de Clientes:", df)
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")

elif menu == "Mis Clientes":
    st.subheader("Mis Clientes y Chat")
    st.write("Selecciona un cliente para ver su historial.")

elif menu == "Carga Masiva":
    st.subheader("Carga de Nuevos Clientes")
    uploaded_file = st.file_uploader("Cargar Excel", type=["xlsx"])
    if uploaded_file:
        st.success("Archivo subido. Procesando integración...")
