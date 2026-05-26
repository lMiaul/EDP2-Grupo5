import streamlit as st

# Verificación de seguridad (Guardián)
if not st.session_state.get("autenticado") or st.session_state.get("rol") != "Acopiador":
    st.warning("⚠️ Acceso denegado. Por favor, inicia sesión como Acopiador en la página principal.")
    st.stop() # Esto detiene la ejecución del resto del código en esta página

# ... (Aquí va todo su código de registro) ...