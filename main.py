import streamlit as st
import pandas as pd
import socket
from sqlalchemy import create_engine, text

# 1. Configuración: Fuerza IPv4 para compatibilidad en red
socket.AF_INET = socket.AF_INET
st.set_page_config(page_title="ActivoPay Pro", layout="wide")

# Inicialización del motor de conexión (Secretos gestionados en Streamlit Cloud)
try:
    url_db = st.secrets["connections"]["postgresql"]["url"]
    engine = create_engine(url_db)
except Exception as e:
    st.error("Error al configurar la conexión a la base de datos.")
    st.stop()

st.title("🚀 Gestión ActivoPay: Ecosistema Digital")

# --- Módulos de Soporte ---

# Regla de Inmutabilidad: Evita duplicados críticos
def validar_duplicado(rif, telefono, ci):
    with engine.connect() as conn:
        query = text("""
            SELECT 'empresa' FROM empresas WHERE rif = :rif OR telefono = :tel 
            UNION SELECT 'usuario' FROM usuarios WHERE ci = :ci
        """)
        resultado = conn.execute(query, {"rif": rif, "tel": telefono, "ci": ci}).fetchone()
        return resultado is not None

# 2. Sidebar de Navegación (Flujo de Trabajo)
menu = st.sidebar.selectbox("Módulo Funcional", ["Dashboard", "Registro", "Gestión Técnica", "Chat de Trazabilidad", "Carga Masiva"])

# --- Ejecución de Módulos ---

# Módulo Analítico (KPIs para Junta Directiva)
if menu == "Dashboard":
    st.subheader("📊 Indicadores de Gestión (KPIs)")
    with engine.connect() as conn:
        df_kpi = pd.read_sql("SELECT estatus, COUNT(*) as total FROM gestion GROUP BY estatus", conn)
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(df_kpi.set_index('estatus'))
        with col2:
            st.table(df_kpi)

# Módulo de Ingesta (Registro)
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
                st.error("Error: Conflicto de datos. El registro ya existe.")
            else:
                with engine.connect() as conn:
                    conn.execute(text("INSERT INTO empresas (rif, nombre, telefono) VALUES (:rif, :n, :t)"), 
                                 {"rif": rif, "n": nombre, "t": telefono})
                    conn.execute(text("INSERT INTO gestion (empresa_rif, estatus) VALUES (:rif, 'Pendiente')"), 
                                 {"rif": rif})
                    conn.commit()
                st.success("Cliente registrado con éxito.")

# Módulo de Gestión (Transiciones de Estado)
elif menu == "Gestión Técnica":
    st.subheader("Control de Afiliación Administrativa")
    with engine.connect() as conn:
        data = pd.read_sql("SELECT g.id_gestion, e.nombre, g.estatus FROM gestion g JOIN empresas e ON g.empresa_rif = e.rif", conn)
    st.table(data)
    
    id_g = st.number_input("ID Gestión a actualizar", min_value=1)
    accion = st.selectbox("Cambiar Estatus", ["Pendiente", "Aprobado", "Rechazado", "En Producción"])
    obs = st.text_area("Observaciones")
    
    if st.button("Actualizar y Notificar"):
        with engine.connect() as conn:
            conn.execute(text("UPDATE gestion SET estatus = :s, observaciones = :o WHERE id_gestion = :id"), 
                         {"s": accion, "o": obs, "id": id_g})
            conn.commit()
        st.success("Estado actualizado.")

# Módulo de Trazabilidad (Chat)
elif menu == "Chat de Trazabilidad":
    st.subheader("Historial de Mensajes y Observaciones")
    id_g = st.text_input("ID de Gestión")
    if id_g:
        with engine.connect() as conn:
            mensajes = pd.read_sql("SELECT remitente, mensaje, fecha FROM historial_mensajes WHERE gestion_id = :id", conn, params={"id": id_g})
        st.table(mensajes)
        msg = st.text_input("Nuevo mensaje:")
        if st.button("Enviar"):
            with engine.connect() as conn:
                conn.execute(text("INSERT INTO historial_mensajes (gestion_id, remitente, mensaje) VALUES (:id, 'Admin', :msg)"), 
                             {"id": id_g, "msg": msg})
                conn.commit()
            st.rerun()

# Módulo de Migración (Carga Masiva - Normalización)
elif menu == "Carga Masiva":
    st.subheader("Migración de Datos Históricos")
    uploaded_file = st.file_uploader("Cargar Excel Histórico", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        if st.button("Normalizar y Migrar"):
            try:
                with engine.begin() as conn:
                    for _, row in df.iterrows():
                        conn.execute(text("INSERT INTO empresas (rif, nombre, telefono) VALUES (:rif, :nom, :tel) ON CONFLICT DO NOTHING"), 
                                     {"rif": row['RIF'], "nom": row['Nombre'], "tel": row['Telefono']})
                        conn.execute(text("INSERT INTO gestion (empresa_rif, estatus) VALUES (:rif, 'En Producción') ON CONFLICT DO NOTHING"), 
                                     {"rif": row['RIF']})
                st.success("Migración finalizada con éxito.")
            except Exception as e:
                st.error(f"Error en migración: {e}")
