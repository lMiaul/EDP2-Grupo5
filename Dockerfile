# Usar una imagen base oficial de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos primero (para aprovechar la caché de Docker)
COPY requirements.txt /app/

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación al directorio de trabajo
COPY . /app/

# Exponer el puerto que usa Streamlit por defecto
EXPOSE 8501

# Comando para ejecutar la aplicación de Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
