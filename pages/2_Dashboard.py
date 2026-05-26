import streamlit as st

# Verificación de seguridad (Guardián)
if not st.session_state.get("autenticado") or st.session_state.get("rol") != "Administrador":
    st.warning("⚠️ Acceso denegado. Por favor, inicia sesión como Administrador en la página principal.")
    st.stop()

# ... (Aquí va todo su código de KPIs y Pandas) ...