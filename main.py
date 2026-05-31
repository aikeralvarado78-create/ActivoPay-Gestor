import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Configuración
st.set_page_config(page_title="ActivoPay Pro", layout="wide")
url_db = st.secrets["connections"]["postgresql"]["url"]
engine = create_engine(url_db)

st.title("🚀 ActivoPay: Ecosistema Digital")

# Módulo de Validación de Inmutabilidad
def validar_duplicado(rif, telefono, ci):
    with engine.connect() as conn:
        check = conn.execute(text(
            "SELECT 'empresa' FROM empresas WHERE rif = :rif OR telefono = :tel "
            "UNION SELECT 'usuario' FROM usuarios WHERE ci = :ci"
        ), {"rif": rif, "tel": telefono, "ci": ci}).fetchone()
        return check is not None

menu = st.sidebar.selectbox("Módulo", ["Dashboard", "Registro", "Gestión Técnica", "Chat"])

# Módulo de Registro (Ingesta)
if menu == "Registro":
    st.subheader("Registro de Nuevo Cliente")
    with st.form("registro_form"):
        rif = st.text_input("RIF")
        nombre = st.text_input("Nombre Empresa")
        telefono = st.text_input("Teléfono")
        ci = st.text_input("Cédula Representante")
        submit = st.form_submit_button("Registrar")
        
        if submit:
            if validar_duplicado(rif, telefono, ci):
                st.error("Error: Conflicto de datos (RIF, Teléfono o Cédula ya existen).")
            else:
                with engine.connect() as conn:
                    conn.execute(text("INSERT INTO empresas (rif, nombre, telefono) VALUES (:rif, :n, :t)"), 
                                 {"rif": rif, "n": nombre, "t": telefono})
                    conn.execute(text("INSERT INTO gestion (empresa_rif, estatus) VALUES (:rif, 'Pendiente')"), 
                                 {"rif": rif})
                    conn.commit()
                st.success("Cliente registrado correctamente.")

# Módulo de Gestión (Administrativa)
elif menu == "Gestión Técnica":
    st.subheader("Control de Afiliación")
    with engine.connect() as conn:
        data = pd.read_sql("SELECT * FROM gestion", conn)
    
    st.table(data)
    id_g = st.number_input("ID Gestión a procesar", min_value=1)
    accion = st.selectbox("Cambiar Estatus", ["Pendiente", "Aprobado", "Rechazado", "En Producción"])
    
    if st.button("Actualizar Estatus"):
        with engine.connect() as conn:
            conn.execute(text("UPDATE gestion SET estatus = :s WHERE id_gestion = :id"), {"s": accion, "id": id_g})
            conn.commit()
        st.experimental_rerun()
