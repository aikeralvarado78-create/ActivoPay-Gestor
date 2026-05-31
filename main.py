import streamlit as st
from sqlalchemy import text

# 1. Configuración de página (debe ser la primera instrucción)
st.set_page_config(page_title="ActivoPay Gestor", layout="wide")

# 2. Inicialización de la conexión a Supabase
# Asegúrate de tener la URL configurada en los Secrets con el puerto 6543
conn = st.connection("postgresql", type="sql")

st.title("🚀 Gestión ActivoPay")

# 3. Verificación de conexión (opcional, puedes borrar esto una vez que funcione)
try:
    with conn.session as s:
        s.execute(text("SELECT 1"))
except Exception as e:
    st.error(f"Error técnico de conexión: {e}")

# 4. Sidebar para Navegación
menu = st.sidebar.selectbox("Menú Principal", ["Dashboard", "Mis Clientes", "Carga Masiva"])

# 5. Lógica del Dashboard
if menu == "Dashboard":
    st.subheader("Reporte de Gestión")
    try:
        # Consulta SQL correcta usando text()
        df = conn.query(text("SELECT * FROM empresas LIMIT 10;"))
        st.write("Resumen de Clientes:", df)
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")

# 6. Lógica de Mis Clientes
elif menu == "Mis Clientes":
    st.subheader("Mis Clientes y Chat")
    st.write("Selecciona un cliente para ver su historial.")

# 7. Lógica de Carga Masiva
elif menu == "Carga Masiva":
    st.subheader("Carga de Nuevos Clientes")
    uploaded_file = st.file_uploader("Cargar Excel", type=["xlsx"])
    if uploaded_file:
        st.success("Archivo subido. Procesando integración...")

# 8. Función para el Chat
def renderizar_chat(id_gestion):
    st.write("---")
    st.subheader("Historial de Comunicación")
    mensaje = st.text_input("Enviar observación al equipo...")
    if st.button("Enviar"):
        st.write("Mensaje enviado al equipo administrativo.")
