import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="ActivoPay Gestor", layout="wide")

# 2. Inicialización de la conexión
# Asegúrate de que en 'Secrets' la URL tenga el puerto 6543
try:
    conn = st.connection("postgresql", type="sql")
except Exception as e:
    st.error(f"Error al iniciar conexión: {e}")
    st.stop()

st.title("🚀 Gestión ActivoPay")

# 3. Navegación
menu = st.sidebar.selectbox("Menú Principal", ["Dashboard", "Mis Clientes", "Carga Masiva"])

# 4. Lógica del Dashboard
if menu == "Dashboard":
    st.subheader("Reporte de Gestión")
    try:
        # Consulta SQL como string simple
        df = conn.query("SELECT * FROM empresas LIMIT 10;")
        st.write("Resumen de Clientes:", df)
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")

# 5. Lógica de Mis Clientes
elif menu == "Mis Clientes":
    st.subheader("Mis Clientes y Chat")
    st.write("Selecciona un cliente para ver su historial.")

# 6. Lógica de Carga Masiva
elif menu == "Carga Masiva":
    st.subheader("Carga de Nuevos Clientes")
    uploaded_file = st.file_uploader("Cargar Excel", type=["xlsx"])
    if uploaded_file:
        st.success("Archivo subido. Procesando integración...")

# 7. Función para el Chat
def renderizar_chat(id_gestion):
    st.write("---")
    st.subheader("Historial de Comunicación")
    mensaje = st.text_input("Enviar observación al equipo...")
    if st.button("Enviar"):
        st.write("Mensaje enviado al equipo administrativo.")
