import os
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env (si existe)
load_dotenv()

def obtener_configuracion(clave):
    """
    Busca la configuración en este orden de prioridad:
    1. Variables de entorno (Útil para Docker o archivo .env).
    2. Secretos de Streamlit (Útil para .streamlit/secrets.toml).
    """
    valor = os.getenv(clave)
    if valor:
        return valor
        
    if clave in st.secrets:
        return st.secrets[clave]
        
    return None

# El decorador @st.cache_resource es CRÍTICO. 
# Le dice a Streamlit: "Ejecuta esta función de conexión solo una vez por sesión, 
# y reutiliza la conexión en lugar de crear una nueva con cada clic."
@st.cache_resource(show_spinner="Conectando a la base de datos...")
def init_connection():
    # 1. Buscamos la URL usando nuestra función híbrida
    url = obtener_configuracion("MONGO_URL")
    
    if not url:
        st.error("⚠️ Error: No se encontró la variable MONGO_URL en el entorno ni en secrets.")
        st.stop()  # Detiene la ejecución de la app
        
    try:
        # Inicializamos el cliente de MongoDB
        client = MongoClient(url)
        # Hacemos un 'ping' rápido para confirmar que el servidor responde
        client.admin.command('ping')
        return client
    except ConnectionFailure as e:
        st.error(f"❌ Error conectando a MongoDB. Verifica que Docker/Mongo esté corriendo. Detalle: {e}")
        st.stop()

# 2. Obtenemos el cliente (la conexión global)
client = init_connection()

# 3. Seleccionamos la base de datos usando la función híbrida (o por defecto "cac_valleverde")
db_name = obtener_configuracion("DB_NAME") or "cac_valleverde"
db = client[db_name]

# 4. Exportamos las colecciones directamente para que los desarrolladores las importen
col_acopios = db["acopios"]
col_agricultores = db["agricultores"]
col_usuarios = db["usuarios"]