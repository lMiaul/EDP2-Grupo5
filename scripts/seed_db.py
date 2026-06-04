# scripts/seed_db.py
"""
Script de seed para poblar MongoDB con datos de demostración.
Uso: python scripts/seed_db.py
Se ejecuta automáticamente si se configura como entrypoint.
"""
import os
import random
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME", "cac_valleverde")

def seed():
    client = MongoClient(MONGODB_URL)
    db = client[DB_NAME]

    # Solo poblar si la colección está vacía (idempotente)
    if db.agricultores.count_documents({}) > 0:
        print("ℹ️  La base de datos ya tiene datos. Seed omitido.")
        client.close()
        return

    # ... lógica de generación de agricultores y acopios ...
    print("✅ Seed completado exitosamente.")
    client.close()

if __name__ == "__main__":
    seed()
