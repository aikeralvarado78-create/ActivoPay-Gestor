import streamlit as st
import pandas as pd
# from database import session, Empresa, Gestion # Aquí importarás tus conexiones

st.set_page_config(page_title="ActivoPay Gestor", layout="wide")

st.title("🚀 Gestión ActivoPay")

# 1. Sidebar para Navegación
menu = st.sidebar.selectbox("Menú Principal", ["Dashboard", "Mis Clientes", "Carga Masiva"])

if menu == "Dashboard":
    st.subheader("Reporte de Gestión")
    # Aquí irán los gráficos y KPIs
    st.write("Visualización de KPIs en tiempo real...")

elif menu == "Mis Clientes":
    st.subheader("Mis Clientes y Chat")
    # Tabla de clientes
    # Al seleccionar un cliente, se debe desplegar el historial de mensajes
    st.write("Selecciona un cliente para ver su historial y estado.")

elif menu == "Carga Masiva":
    st.subheader("Carga de Nuevos Clientes")
    uploaded_file = st.file_uploader("Cargar Excel", type=["xlsx"])
    if uploaded_file:
        # Aquí llamaríamos a la función de migración que documentamos
        st.success("Archivo procesado. Verificando duplicados...")

# 2. Lógica del Chat (Ejemplo conceptual)
def renderizar_chat(id_gestion):
    st.write("---")
    st.subheader("Historial de Comunicación")
    # Aquí consultaríamos la tabla Historial_Mensajes
    mensaje = st.text_input("Enviar observación al equipo...")
    if st.button("Enviar"):
        # Lógica para guardar en la BD
        st.write("Mensaje enviado al equipo administrativo.")