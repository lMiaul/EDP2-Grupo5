import os
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# El decorador @st.cache_resource es CRÍTICO. 
# Le dice a Streamlit: "Ejecuta esta función de conexión solo una vez por sesión, 
# y reutiliza la conexión en lugar de crear una nueva con cada clic."
@st.cache_resource(show_spinner="Conectando a la base de datos...")
def init_connection():
    uri = os.getenv("MONGO_URI")
    if not uri:
        st.error("⚠️ Error: No se encontró la variable MONGO_URI en el archivo .env")
        st.stop()  # Detiene la ejecución de la app
        
    try:
        # Inicializamos el cliente de MongoDB
        client = MongoClient(uri)
        # Hacemos un 'ping' rápido para confirmar que el servidor responde
        client.admin.command('ping')
        return client
    except ConnectionFailure as e:
        st.error(f"❌ Error conectando a MongoDB. Verifica que Docker/Mongo esté corriendo. Detalle: {e}")
        st.stop()

# 1. Obtenemos el cliente (la conexión global)
client = init_connection()

# 2. Seleccionamos la base de datos usando la variable del .env (o por defecto "cac_valleverde")
db_name = os.getenv("DB_NAME", "cac_valleverde")
db = client[db_name]

# 3. Exportamos las colecciones directamente para que los desarrolladores las importen
col_acopios = db["acopios"]
col_agricultores = db["agricultores"]