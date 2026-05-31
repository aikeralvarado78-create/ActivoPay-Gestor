import streamlit as st

# Configuración inicial
st.set_page_config(page_title="ActivoPay Gestor", layout="wide")

# Inicialización de conexión
conn = st.connection("postgresql", type="sql")

st.title("🚀 Gestión ActivoPay")

menu = st.sidebar.selectbox("Menú Principal", ["Dashboard", "Mis Clientes", "Carga Masiva"])

if menu == "Dashboard":
    st.subheader("Reporte de Gestión")
    try:
        # Usamos el string plano para evitar errores de hashing
        # La IP forzada en secrets resolverá el problema de conexión
        df = conn.query("SELECT * FROM empresas LIMIT 10;")
        st.write("Resumen de Clientes:", df)
    except Exception as e:
        st.error(f"Error técnico al cargar: {e}")

elif menu == "Mis Clientes":
    st.subheader("Mis Clientes y Chat")
    st.write("Selecciona un cliente para ver su historial.")

elif menu == "Carga Masiva":
    st.subheader("Carga de Nuevos Clientes")
    uploaded_file = st.file_uploader("Cargar Excel", type=["xlsx"])
    if uploaded_file:
        st.success("Archivo subido.")
