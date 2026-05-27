import streamlit as st
import pandas as pd
from database import col_acopios

# Verificación de seguridad (Guardián)
if not st.session_state.get("autenticado") or st.session_state.get("rol") != "Administrador":
    st.warning("⚠️ Acceso denegado. Por favor, inicia sesión como Administrador en la página principal.")
    st.stop()

# Extraer datos de MongoDB
cursor = col_acopios.find({}, {"_id": 0})
datos_lista = list(cursor)

# Verificar si existen datos
if not datos_lista:
    st.warning("No hay datos de acopio registrados aún.")
    st.stop()

# Convertir JSON a DataFrame
df = pd.json_normalize(datos_lista)

# Convertir fecha
if 'fecha_registro' in df.columns:
    df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])

# Renombrar columnas
df = df.rename(columns={
    'agricultor.nombre_completo': 'Agricultor',
    'agricultor.sector_comunidad': 'Sector',
    'agricultor.tipo_cacao': 'Tipo de Cacao',
    'datos_pesaje.peso_neto_total_kg': 'Peso Neto (Kg)',
    'control_calidad.estado_lote': 'Estado',
    'valores_comerciales.monto_total_pagar': 'Monto Total (S/.)'
})

# =========================
# TÍTULO
# =========================

st.title("📊 Dashboard Administrativo")
st.markdown("Panel gerencial para monitoreo de inventario, calidad y pagos.")

# =========================
# KPIs
# =========================

total_kg = df['Peso Neto (Kg)'].sum()
total_pago = df['Monto Total (S/.)'].sum()
total_registros = len(df)
lotes_observados = (df['Estado'] != "Aprobado").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌱 Kg Acopiados", f"{total_kg:,.2f} kg")
col2.metric("💰 Pagos Totales", f"S/ {total_pago:,.2f}")
col3.metric("📦 Registros", total_registros)
col4.metric("⚠️ Lotes Observados", lotes_observados)

st.divider()

# =========================
# GRÁFICOS
# =========================

st.subheader("📌 Acopio por Sector")

sector_chart = df.groupby('Sector')['Peso Neto (Kg)'].sum()
st.bar_chart(sector_chart)

st.subheader("📌 Estado de Calidad")

estado_chart = df['Estado'].value_counts()
st.bar_chart(estado_chart)

st.subheader("📌 Tipo de Cacao")

tipo_chart = df['Tipo de Cacao'].value_counts()
st.bar_chart(tipo_chart)

st.divider()

# =========================
# TABLA
# =========================

st.subheader("📋 Registros de Acopio")

st.dataframe(
    df[[
        'fecha_registro',
        'Agricultor',
        'Sector',
        'Tipo de Cacao',
        'Peso Neto (Kg)',
        'Estado',
        'Monto Total (S/.)'
    ]],
    use_container_width=True
)