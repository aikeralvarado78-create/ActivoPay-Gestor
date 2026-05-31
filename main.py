import streamlit as st
import pandas as pd
import socket
from sqlalchemy import create_engine, text

# 1. Configuración de Red y Página
socket.AF_INET = socket.AF_INET
st.set_page_config(page_title="ActivoPay Pro", layout="wide")

# Inicialización del motor de conexión
try:
    url_db = st.secrets["connections"]["postgresql"]["url"]
    engine = create_engine(url_db)
except Exception as e:
    engine = None
    st.error("Error de configuración de BD. Revisa los Secrets.")

st.title("🚀 Gestión ActivoPay: Ecosistema Digital")

# 2. Sidebar de Navegación
menu = st.sidebar.selectbox("Módulo", ["Dashboard", "Registro", "Gestión Técnica", "Carga Masiva"])

# Módulo de Validación de Inmutabilidad
def validar_duplicado(rif, telefono, ci):
    with engine.connect() as conn:
        query = text("""
            SELECT 'empresa' FROM empresas WHERE rif = :rif OR telefono = :tel 
            UNION SELECT 'usuario' FROM usuarios WHERE ci = :ci
        """)
        result = conn.execute(query, {"rif": rif, "tel": telefono, "ci": ci}).fetchone()
        return result is not None

# 3. Módulos Funcionales
if menu == "Dashboard":
    st.subheader("📊 Indicadores de Gestión (KPIs)")
    if engine:
        with engine.connect() as conn:
            df_kpi = pd.read_sql("SELECT estatus, COUNT(*) as total FROM gestion GROUP BY estatus", conn)
            col1, col2 = st.columns(2)
            with col1:
                st.bar_chart(df_kpi.set_index('estatus'))
            with col2:
                st.table(df_kpi)
    else:
        st.info("Configura la BD para ver los KPIs.")

elif menu == "Registro":
    st.subheader("Registro de Nuevo Cliente")
    with st.form("registro_form"):
        rif = st.text_input("RIF")
        nombre = st.text_input("Nombre Empresa")
        telefono = st.text_input("Teléfono")
        ci = st.text_input("Cédula Representante")
        submit = st.form_submit_button("Registrar")
        if submit:
            if validar_duplicado(rif, telefono, ci):
                st.error("Error: Conflicto de datos (RIF, Teléfono o Cédula duplicados).")
            else:
                with engine.connect() as conn:
                    conn.execute(text("INSERT INTO empresas (rif, nombre, telefono) VALUES (:rif, :n, :t)"), 
                                 {"rif": rif, "n": nombre, "t": telefono})
                    conn.execute(text("INSERT INTO gestion (empresa_rif, estatus) VALUES (:rif, 'Pendiente')"), 
                                 {"rif": rif})
                    conn.commit()
                st.success("Cliente registrado con éxito.")

elif menu == "Gestión Técnica":
    st.subheader("Control de Afiliación")
    if engine:
        with engine.connect() as conn:
            data = pd.read_sql("SELECT * FROM gestion", conn)
        st.table(data)
        id_g = st.number_input("ID Gestión a procesar", min_value=1)
        accion = st.selectbox("Cambiar Estatus", ["Pendiente", "Aprobado", "Rechazado", "En Producción"])
        if st.button("Actualizar Estatus"):
            with engine.connect() as conn:
                conn.execute(text("UPDATE gestion SET estatus = :s WHERE id_gestion = :id"), {"s": accion, "id": id_g})
                conn.commit()
            st.rerun()

elif menu == "Carga Masiva":
    st.subheader("Carga de Excel")
    uploaded_file = st.file_uploader("Cargar Excel", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.write("Vista previa:", df.head())
        if st.button("Guardar en Base de Datos"):
            if engine:
                df.to_sql('clientes_tmp', engine, if_exists='append', index=False)
                st.success("¡Datos procesados correctamente!")
            else:
                st.error("Sin conexión a BD.")
