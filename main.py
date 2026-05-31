import streamlit as st

# 1. ESTO DEBE IR PRIMERO SIEMPRE
st.set_page_config(page_title="ActivoPay Gestor", layout="wide")

# 2. Ahora inicializamos la conexión
conn = st.connection("postgresql", type="sql")

st.title("🚀 Gestión ActivoPay")

# 3. Prueba de conexión (oculta si ya confirmaste que funciona)
try:
    with conn.session as s:
        s.execute("SELECT 1")
    # st.success("¡Conexión establecida!") # Puedes comentar esta línea después de verificar
except Exception as e:
    st.error(f"Error técnico de conexión: {e}")

# 4. Sidebar para Navegación
menu = st.sidebar.selectbox("Menú Principal", ["Dashboard", "Mis Clientes", "Carga Masiva"])

if menu == "Dashboard":
    st.subheader("Reporte de Gestión")
    try:
        df = conn.query("SELECT * FROM empresas LIMIT 10;")
        st.write("Resumen de Clientes:", df)
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")

# ... resto de tu código
