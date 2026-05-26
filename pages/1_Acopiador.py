import streamlit as st
import pandas as pd
from datetime import datetime, timezone
import random # Para simular tickets y lotes
from database import col_acopios, col_agricultores

# ==========================================
# 1. SEGURIDAD Y CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Acopio | LogiStock", page_icon="📝", layout="wide")

if not st.session_state.get("autenticado") or st.session_state.get("rol") != "Acopiador":
    st.warning("⚠️ Acceso denegado. Por favor, inicia sesión como Acopiador en la página principal.")
    st.stop()

st.title("📝 Registro Rápido de Acopio")
st.markdown("Ingrese los datos físicos y de calidad del cacao recibido.")

# ==========================================
# 2. CARGA DE DATOS MAESTROS (Agricultores)
# ==========================================
@st.cache_data(ttl=60) # Cacheamos por 60s para no saturar la BD
def obtener_agricultores():
    # Traemos todos los agricultores y los formateamos para el Selectbox
    cursor = col_agricultores.find({}, {"_id": 0})
    return list(cursor)

lista_agricultores = obtener_agricultores()

if not lista_agricultores:
    st.error("No hay agricultores registrados en la base de datos. Ejecuta el Seed primero.")
    st.stop()

# Crear un diccionario para acceder fácil a los datos del agricultor elegido
dict_agricultores = {f"{a['nombre_completo']} ({a['dni_ruc']})": a for a in lista_agricultores}

# ==========================================
# 3. INTERFAZ DE REGISTRO
# ==========================================
# Usamos contenedores y columnas para una UI compacta

# Función callback para limpiar el formulario
def limpiar_formulario():
    # Solo reseteamos la variable específica de la cantidad de sacos
    st.session_state["input_cantidad_sacos"] = 1

col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Datos del Productor")
    agric_seleccionado = st.selectbox("Buscar Agricultor:", options=list(dict_agricultores.keys()))
    datos_agric = dict_agricultores[agric_seleccionado]
    
    # MEJORA UX: Tarjeta de información estructurada en columnas
    with st.container(border=True): # Agrega un borde sutil estilo tarjeta
        st.markdown(f"**Productor:** {datos_agric['nombre_completo']}")
        
        # Subcolumnas para separar la información clave
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.caption("📍 Sector")
            st.write(f"**{datos_agric['sector_comunidad']}**")
        with info_col2:
            st.caption("🆔 Código")
            st.write(f"**{datos_agric['codigo_productor']}**")
        with info_col3:
            st.caption("🏷️ Certificación")
            # Si no hay, muestra un guión para mantener el diseño limpio
            cert = ', '.join(datos_agric['certificaciones']) if datos_agric['certificaciones'] else "-"
            st.write(f"**{cert}**")

with col2:
    st.subheader("🔬 Control de Calidad")
    humedad = st.number_input("% Humedad", min_value=0.0, max_value=30.0, value=7.5, step=0.1)
    impurezas = st.number_input("% Impurezas", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
    fermentacion = st.selectbox("Grado Fermentación", ["Tipo 1 (Premium)", "Tipo 2 (Estándar)"])

st.divider()

st.subheader("⚖️ Pesaje Físico")
# Añadimos key="input_cantidad_sacos"
cantidad_sacos = st.number_input("Cantidad de Sacos a pesar", min_value=1, max_value=20, value=1, step=1, key="input_cantidad_sacos")

# Generar inputs dinámicos según la cantidad de sacos
detalle_sacos = []
peso_bruto_total = 0.0

# Creamos columnas dinámicas (máximo 5 por fila para no romper la pantalla)
cols_sacos = st.columns(min(cantidad_sacos, 5)) 
for i in range(cantidad_sacos):
    with cols_sacos[i % 5]:
        peso = st.number_input(f"Peso Saco {i+1} (Kg)", min_value=1.0, max_value=100.0, value=60.0, step=0.5, key=f"saco_{i}")
        detalle_sacos.append({"nro_saco": i+1, "peso_bruto_kg": round(peso, 2)})
        peso_bruto_total += peso

# --- LÓGICA DE NEGOCIO Y CÁLCULOS AUTOMÁTICOS ---
tara_por_saco = 0.5 # 500 gramos por saco vacío
tara_total = cantidad_sacos * tara_por_saco
peso_neto_total = peso_bruto_total - tara_total

estado_lote = "Aprobado" if humedad <= 8.0 else "Observado (Requiere secado)"

# Finanzas
precio_base = 12.00
bono_cert = 1.50 if "Orgánico" in datos_agric['certificaciones'] else 0.0
descuento_hum = 0.50 if humedad > 8.0 else 0.0
precio_final = precio_base + bono_cert - descuento_hum
monto_pagar = peso_neto_total * precio_final

# Mostrar resumen al operario antes de guardar
with st.expander("📊 Ver Resumen de Transacción y Pagos", expanded=True):
    r_col1, r_col2, r_col3 = st.columns(3)
    r_col1.metric("Peso Neto Total", f"{peso_neto_total:.2f} Kg")
    r_col2.metric("Precio Final / Kg", f"S/ {precio_final:.2f}")
    r_col3.metric("Monto a Pagar", f"S/ {monto_pagar:.2f}")

# ==========================================
# 4. GUARDAR EN BASE DE DATOS
# ==========================================
if st.button("💾 Registrar Ingreso de Cacao", type="primary", use_container_width=True):
    
    # Armamos el JSON exactamente como la estructura requerida
    nuevo_acopio = {
        "codigo_ticket": f"TK-2026-{random.randint(1000, 9999)}",
        "fecha_registro": datetime.now(timezone.utc),
        "operario_id": st.session_state.get("operario_id", "usr_desconocido"),
        "agricultor": {
            "agricultor_id": datos_agric["agricultor_id"],
            "nombre_completo": datos_agric["nombre_completo"],
            "dni_ruc": datos_agric["dni_ruc"],
            "codigo_productor": datos_agric["codigo_productor"],
            "certificaciones": datos_agric["certificaciones"],
            "sector_comunidad": datos_agric["sector_comunidad"],
            "tipo_cacao": datos_agric["tipo_cacao"]
        },
        "datos_pesaje": {
            "cantidad_sacos": cantidad_sacos,
            "detalle_sacos": detalle_sacos,
            "peso_bruto_total_kg": round(peso_bruto_total, 2),
            "tara_total_kg": round(tara_total, 2),
            "peso_neto_total_kg": round(peso_neto_total, 2)
        },
        "control_calidad": {
            "porcentaje_humedad": round(humedad, 1),
            "porcentaje_impurezas": round(impurezas, 1),
            "grado_fermentacion": fermentacion,
            "estado_lote": estado_lote
        },
        "valores_comerciales": {
            "precio_base_por_kilo": precio_base,
            "bonificacion_certificacion": bono_cert,
            "descuento_humedad": descuento_hum,
            "precio_final_por_kilo": precio_final,
            "monto_total_pagar": round(monto_pagar, 2)
        },
        "trazabilidad": {
            "codigo_lote_exportacion": f"LOTE-EXP-2026-{datetime.now().strftime('%b').upper()}-{random.randint(1,10)}",
            "ubicacion_almacen": "ZONA-A-RECEPCION"
        },
        "metadata_sistema": {
            "dispositivo_registro": "Terminal-Web-01",
            "estado_pago": "Pendiente",
            "ultima_modificacion": datetime.now(timezone.utc)
        }
    }
    
    try:
        col_acopios.insert_one(nuevo_acopio)
        st.success(f"✅ ¡Acopio registrado con éxito! Ticket: {nuevo_acopio['codigo_ticket']}")
        st.balloons()
        
        # Invocamos la limpieza de las variables del estado
        limpiar_formulario()
        
        # Usamos st.rerun() para forzar a Streamlit a recargar la página 
        # y aplicar inmediatamente el valor de "1" en el input de sacos.
        st.rerun() 
        
    except Exception as e:
        st.error(f"❌ Error al guardar en la base de datos: {e}")