import streamlit as st

# La conexión buscará automáticamente el puerto 6543 que pusimos en los Secrets
conn = st.connection("postgresql", type="sql")

# Prueba la conexión
try:
    with conn.session as s:
        s.execute("SELECT 1")
    st.success("¡Conexión establecida exitosamente!")
except Exception as e:
    st.error(f"Error técnico de conexión: {e}")

st.set_page_config(page_title="ActivoPay Gestor", layout="wide")

st.title("🚀 Gestión ActivoPay")

# 2. Sidebar para Navegación
menu = st.sidebar.selectbox("Menú Principal", ["Dashboard", "Mis Clientes", "Carga Masiva"])

if menu == "Dashboard":
    st.subheader("Reporte de Gestión")
    # Ejemplo de cómo consultar datos de tu BD
    try:
        # Reemplaza 'empresas' por el nombre de tu tabla real
        df = conn.query("SELECT * FROM empresas LIMIT 10;")
        st.write("Resumen de Clientes:", df)
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")

elif menu == "Mis Clientes":
    st.subheader("Mis Clientes y Chat")
    # Aquí consultarías tu tabla de clientes
    st.write("Selecciona un cliente para ver su historial.")

elif menu == "Carga Masiva":
    st.subheader("Carga de Nuevos Clientes")
    uploaded_file = st.file_uploader("Cargar Excel", type=["xlsx"])
    if uploaded_file:
        st.success("Archivo subido. Procesando integración...")
